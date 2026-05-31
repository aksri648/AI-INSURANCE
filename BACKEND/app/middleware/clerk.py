from fastapi import Request, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.config import settings
from app.database import async_session
from app.models import User
from sqlalchemy import select
import httpx
from loguru import logger

security = HTTPBearer(auto_error=False)


async def verify_clerk_token(credentials: HTTPAuthorizationCredentials = Depends(security)) -> dict:
    if not credentials:
        raise HTTPException(status_code=401, detail="Authentication required")

    token = credentials.credentials

    try:
        from clerk_backend_api import Clerk
        from clerk_backend_api.security import authenticate_request
        from clerk_backend_api.security.types import AuthenticateRequestOptions

        sdk = Clerk(bearer_auth=settings.clerk_api_key)

        request_state = sdk.authenticate_request(
            token,
            AuthenticateRequestOptions(
                authorized_parties=settings.cors_origins
            )
        )

        if request_state.is_signed_in:
            return request_state.payload or {}
        else:
            raise HTTPException(status_code=401, detail=f"Authentication failed: {request_state.reason}")

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Auth verification failed: {e}")
        raise HTTPException(status_code=401, detail="Authentication failed")


async def get_current_user(clerk_data: dict = Depends(verify_clerk_token)) -> User:
    clerk_id = clerk_data.get("sub", clerk_data.get("user_id", ""))
    if not clerk_id:
        raise HTTPException(status_code=401, detail="Invalid authentication data")

    async with async_session() as session:
        result = await session.execute(select(User).where(User.clerk_id == clerk_id))
        user = result.scalar_one_or_none()

        if not user:
            email = clerk_data.get("email", clerk_data.get("email_addresses", [{}])[0].get("email_address", ""))
            name = clerk_data.get("name", clerk_data.get("first_name", "") + " " + clerk_data.get("last_name", ""))
            user = User(
                clerk_id=clerk_id,
                email=email,
                name=name.strip() or email.split("@")[0],
            )
            session.add(user)
            await session.commit()
            await session.refresh(user)

        return user
