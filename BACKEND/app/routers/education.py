from fastapi import APIRouter, Depends, HTTPException
from app.middleware.clerk import get_current_user
from app.models import User
from app.schemas.education import EducationQuery, EducationResponse, MisSellingCheckRequest, MisSellingCheckResponse
from app.agents.insurance_education_agent import insurance_education_agent
from app.agents.mis_selling_detection_agent import mis_selling_detection_agent
from app.database import async_session
from app.models import Policy, MisSellingReport
from sqlalchemy import select
from sqlalchemy.orm import selectinload
import json
from loguru import logger

router = APIRouter(prefix="/api/education", tags=["Education"])


@router.post("/explain", response_model=EducationResponse)
async def explain_topic(
    request: EducationQuery,
    user: User = Depends(get_current_user),
):
    try:
        result_text = await insurance_education_agent.explain(
            query=request.query,
            difficulty=request.difficulty,
        )
        data = json.loads(result_text) if isinstance(result_text, str) else result_text

        return EducationResponse(
            topic=data.get("topic", request.query),
            explanation=data.get("explanation", ""),
            key_takeaways=data.get("key_takeaways", []),
            related_topics=data.get("related_topics", []),
            sources=[{"title": k, "content": v} for k, v in data.get("definitions", {}).items()],
            confidence="verified",
        )
    except Exception as e:
        logger.error(f"Education query failed: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to explain: {str(e)}")


@router.post("/mis-selling-check", response_model=MisSellingCheckResponse)
async def check_mis_selling(
    request: MisSellingCheckRequest,
    user: User = Depends(get_current_user),
):
    async with async_session() as session:
        stmt = (
            select(Policy)
            .where(Policy.id == request.policy_id, Policy.user_id == user.id)
            .options(selectinload(Policy.benefits))
        )
        result = await session.execute(stmt)
        policy = result.scalar_one_or_none()
        if not policy:
            raise HTTPException(status_code=404, detail="Policy not found")

    try:
        result_text = await mis_selling_detection_agent.detect_mis_selling(
            policy_data={
                "title": policy.title,
                "insurer": policy.insurer,
                "type": policy.policy_type,
                "structured_data": policy.structured_data,
                "benefits": [
                    {"name": b.name, "description": b.description, "coverage_amount": b.coverage_amount,
                     "exclusions": b.exclusions, "conditions": b.conditions}
                    for b in (policy.benefits or [])
                ],
            },
            extracted_text=policy.extracted_text or "",
        )

        data = json.loads(result_text) if isinstance(result_text, str) else result_text

        report = MisSellingReport(
            user_id=user.id,
            policy_id=policy.id,
            findings=data.get("findings", []),
            severity=data.get("severity", "low"),
            summary=data.get("summary", ""),
            confidence="verified",
            evidence_refs=[f.get("evidence", "") for f in data.get("findings", [])],
        )

        async with async_session() as session:
            session.add(report)
            await session.commit()

        return MisSellingCheckResponse(
            findings=data.get("findings", []),
            severity=data.get("severity", "low"),
            summary=data.get("summary", ""),
            recommendations=data.get("user_actions", data.get("recommendations", [])),
            evidence_refs=[{"evidence": f.get("evidence", ""), "type": f.get("type", "")} for f in data.get("findings", [])],
            confidence="verified",
        )

    except Exception as e:
        logger.error(f"Mis-selling check failed: {e}")
        raise HTTPException(status_code=500, detail=f"Check failed: {str(e)}")


@router.get("/mis-selling-history")
async def get_mis_selling_history(user: User = Depends(get_current_user)):
    async with async_session() as session:
        stmt = (
            select(MisSellingReport)
            .where(MisSellingReport.user_id == user.id)
            .order_by(MisSellingReport.created_at.desc())
            .limit(20)
        )
        result = await session.execute(stmt)
        reports = result.scalars().all()

        history = []
        for r in reports:
            policy = await session.get(Policy, r.policy_id)
            history.append({
                "id": str(r.id),
                "policy_title": policy.title if policy else "Unknown",
                "severity": r.severity,
                "summary": r.summary,
                "findings_count": len(r.findings or []),
                "created_at": r.created_at.isoformat(),
            })
        return history
