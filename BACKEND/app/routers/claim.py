from fastapi import APIRouter, Depends, HTTPException
from app.middleware.clerk import get_current_user
from app.models import User, Policy, ClaimAssessment, Benefit
from app.database import async_session
from app.schemas.claim import ClaimAssessmentRequest, ClaimAssessmentResponse, ClaimHistoryResponse
from app.agents.claims_assessment_agent import claims_assessment_agent
from app.agents.report_generation_agent import report_generation_agent
from sqlalchemy import select
from sqlalchemy.orm import selectinload
import json
from loguru import logger

router = APIRouter(prefix="/api/claims", tags=["Claims"])


@router.post("/assess", response_model=ClaimAssessmentResponse)
async def assess_claim(
    request: ClaimAssessmentRequest,
    user: User = Depends(get_current_user),
):
    async with async_session() as session:
        stmt = (
            select(Policy)
            .where(Policy.id == request.policy_id, Policy.user_id == user.id, Policy.is_active == True)
            .options(selectinload(Policy.benefits))
        )
        result = await session.execute(stmt)
        policy = result.scalar_one_or_none()
        if not policy:
            raise HTTPException(status_code=404, detail="Policy not found")

    benefits_data = [
        {
            "name": b.name,
            "coverage_amount": b.coverage_amount,
            "waiting_period": b.waiting_period,
            "exclusions": b.exclusions,
            "conditions": b.conditions,
            "deductible": b.deductible,
            "copay": b.copay,
            "claim_limit": b.claim_limit,
        }
        for b in (policy.benefits or [])
    ]

    try:
        result_text = await claims_assessment_agent.assess_claim(
            policy_data={
                "title": policy.title,
                "insurer": policy.insurer,
                "type": policy.policy_type,
                "summary": policy.summary,
                "structured_data": policy.structured_data,
            },
            benefits=benefits_data,
            claim_type=request.claim_type,
            claim_amount=str(request.claim_amount) if request.claim_amount else "Not specified",
            description=request.description,
        )

        result = json.loads(result_text) if isinstance(result_text, str) else result_text

        assessment = ClaimAssessment(
            user_id=user.id,
            policy_id=policy.id,
            claim_type=request.claim_type,
            claim_amount=str(request.claim_amount) if request.claim_amount else None,
            description=request.description,
            assessment_result=result,
            eligibility_score=result.get("eligibility_score"),
            estimated_payout=result.get("estimated_payout"),
            confidence="verified",
            evidence_refs=[],
        )

        async with async_session() as session:
            session.add(assessment)
            await session.commit()
            await session.refresh(assessment)

        return ClaimAssessmentResponse(
            id=assessment.id,
            policy_id=policy.id,
            claim_type=request.claim_type,
            claim_amount=assessment.claim_amount,
            eligibility_score=result.get("eligibility_score"),
            estimated_payout=result.get("estimated_payout"),
            assessment_result=result.get("assessment", {}),
            confidence="verified",
            summary=result.get("summary", ""),
            recommendations=result.get("recommendations", []),
            evidence_refs=result.get("evidence_refs", []),
        )

    except Exception as e:
        logger.error(f"Claim assessment failed: {e}")
        raise HTTPException(status_code=500, detail=f"Assessment failed: {str(e)}")


@router.get("/history", response_model=list[ClaimHistoryResponse])
async def get_claim_history(user: User = Depends(get_current_user)):
    async with async_session() as session:
        stmt = (
            select(ClaimAssessment)
            .where(ClaimAssessment.user_id == user.id)
            .order_by(ClaimAssessment.created_at.desc())
            .limit(20)
        )
        result = await session.execute(stmt)
        assessments = result.scalars().all()

        history = []
        for a in assessments:
            policy = await session.get(Policy, a.policy_id)
            history.append(ClaimHistoryResponse(
                id=a.id,
                policy_id=a.policy_id,
                policy_title=policy.title if policy else "Unknown",
                claim_type=a.claim_type,
                eligibility_score=a.eligibility_score,
                estimated_payout=a.estimated_payout,
                created_at=a.created_at.isoformat(),
                confidence=a.confidence,
            ))
        return history


@router.get("/{claim_id}")
async def get_claim_detail(claim_id: str, user: User = Depends(get_current_user)):
    async with async_session() as session:
        stmt = select(ClaimAssessment).where(
            ClaimAssessment.id == claim_id,
            ClaimAssessment.user_id == user.id,
        )
        result = await session.execute(stmt)
        assessment = result.scalar_one_or_none()
        if not assessment:
            raise HTTPException(status_code=404, detail="Claim assessment not found")

        policy = await session.get(Policy, assessment.policy_id)

        return {
            "id": str(assessment.id),
            "policy": {
                "id": str(policy.id) if policy else None,
                "title": policy.title if policy else "Unknown",
            },
            "claim_type": assessment.claim_type,
            "claim_amount": assessment.claim_amount,
            "description": assessment.description,
            "eligibility_score": assessment.eligibility_score,
            "estimated_payout": assessment.estimated_payout,
            "assessment_result": assessment.assessment_result,
            "confidence": assessment.confidence,
            "created_at": assessment.created_at.isoformat(),
        }
