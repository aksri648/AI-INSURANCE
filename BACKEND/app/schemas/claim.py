from pydantic import BaseModel, Field
from typing import Optional
from uuid import UUID


class ClaimAssessmentRequest(BaseModel):
    policy_id: UUID
    claim_type: str = Field(..., max_length=255)
    claim_amount: Optional[float] = None
    description: str = Field(..., max_length=5000)


class ClaimAssessmentResponse(BaseModel):
    id: UUID
    policy_id: UUID
    claim_type: str
    claim_amount: Optional[str] = None
    eligibility_score: Optional[float] = None
    estimated_payout: Optional[str] = None
    assessment_result: dict = {}
    confidence: str
    summary: str = ""
    recommendations: list[str] = []
    evidence_refs: list[dict] = []


class ClaimHistoryResponse(BaseModel):
    id: UUID
    policy_id: UUID
    policy_title: str = ""
    claim_type: str
    eligibility_score: Optional[float] = None
    estimated_payout: Optional[str] = None
    created_at: str
    confidence: str
