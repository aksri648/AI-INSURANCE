from fastapi import APIRouter, Depends, HTTPException
from app.middleware.clerk import get_current_user
from app.models import User
from app.database import async_session
from sqlalchemy import select
from loguru import logger

router = APIRouter(prefix="/api/auth", tags=["Authentication"])


@router.get("/me")
async def get_me(user: User = Depends(get_current_user)):
    return {
        "id": str(user.id),
        "clerk_id": user.clerk_id,
        "email": user.email,
        "name": user.name,
        "avatar_url": user.avatar_url,
        "preferences": user.preferences or {},
        "created_at": user.created_at.isoformat(),
    }


@router.put("/profile")
async def update_profile(data: dict, user: User = Depends(get_current_user)):
    async with async_session() as session:
        db_user = await session.get(User, user.id)
        if not db_user:
            raise HTTPException(status_code=404, detail="User not found")

        if "name" in data:
            db_user.name = data["name"]
        if "avatar_url" in data:
            db_user.avatar_url = data["avatar_url"]
        if "preferences" in data:
            db_user.preferences = {**(db_user.preferences or {}), **data["preferences"]}

        await session.commit()
        await session.refresh(db_user)

    return {
        "id": str(db_user.id),
        "email": db_user.email,
        "name": db_user.name,
        "avatar_url": db_user.avatar_url,
        "preferences": db_user.preferences or {},
    }


@router.get("/stats")
async def get_user_stats(user: User = Depends(get_current_user)):
    async with async_session() as session:
        from app.models import Policy, ClaimAssessment, MisSellingReport
        from sqlalchemy import func

        policy_count = await session.scalar(
            select(func.count(Policy.id)).where(Policy.user_id == user.id, Policy.is_active == True)
        )
        claim_count = await session.scalar(
            select(func.count(ClaimAssessment.id)).where(ClaimAssessment.user_id == user.id)
        )
        report_count = await session.scalar(
            select(func.count(MisSellingReport.id)).where(MisSellingReport.user_id == user.id)
        )

        return {
            "total_policies": policy_count or 0,
            "total_claims": claim_count or 0,
            "total_reports": report_count or 0,
        }
