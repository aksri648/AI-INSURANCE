from fastapi import Request, HTTPException
from app.database import async_session
from app.models import AuditLog
from app.middleware.clerk import get_current_user
import json
from loguru import logger


async def log_audit(
    request: Request,
    user_id: str = None,
    action: str = "",
    resource_type: str = "",
    resource_id: str = None,
    details: dict = None,
    severity: str = "info",
):
    try:
        audit_entry = AuditLog(
            user_id=user_id,
            action=action,
            resource_type=resource_type,
            resource_id=resource_id,
            details=details or {},
            ip_address=request.client.host if request.client else None,
            user_agent=request.headers.get("user-agent"),
            severity=severity,
        )
        async with async_session() as session:
            session.add(audit_entry)
            await session.commit()
    except Exception as e:
        logger.error(f"Audit log failed: {e}")


async def audit_middleware(request: Request, call_next):
    response = await call_next(request)
    if request.method in ("POST", "PUT", "PATCH", "DELETE"):
        try:
            user = await get_current_user(request)
            await log_audit(
                request=request,
                user_id=str(user.id),
                action=f"{request.method}_{request.url.path}",
                resource_type=request.url.path.split("/")[-1],
                details={"path": request.url.path, "status_code": response.status_code},
            )
        except Exception:
            pass
    return response
