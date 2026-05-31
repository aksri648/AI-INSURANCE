from pydantic import BaseModel, Field
from typing import Optional, Any
from uuid import UUID
from datetime import datetime


class BenefitSchema(BaseModel):
    id: Optional[UUID] = None
    name: str
    description: Optional[str] = None
    coverage_amount: Optional[str] = None
    currency: str = "INR"
    waiting_period: Optional[str] = None
    exclusions: Optional[str] = None
    conditions: Optional[str] = None
    claim_limit: Optional[str] = None
    deductible: Optional[str] = None
    copay: Optional[str] = None
    is_sub_limit: bool = False
    parent_benefit: Optional[str] = None
    confidence: str = "verified"

    class Config:
        from_attributes = True


class PolicyChunkSchema(BaseModel):
    id: Optional[UUID] = None
    chunk_index: int
    content: str
    metadata: dict = {}

    class Config:
        from_attributes = True


class PolicyCreate(BaseModel):
    title: str = Field(..., max_length=500)
    insurer: Optional[str] = None
    policy_number: Optional[str] = None
    policy_type: str = "general"


class PolicyResponse(BaseModel):
    id: UUID
    title: str
    insurer: Optional[str] = None
    policy_number: Optional[str] = None
    policy_type: str
    status: str
    file_type: Optional[str] = None
    file_size_bytes: Optional[int] = None
    summary: Optional[str] = None
    page_count: Optional[int] = None
    created_at: datetime
    updated_at: datetime
    benefits: list[BenefitSchema] = []
    structured_data: dict = {}

    class Config:
        from_attributes = True


class PolicyAnalysisRequest(BaseModel):
    policy_id: UUID


class PolicyAnalysisResponse(BaseModel):
    policy_id: UUID
    summary: str
    benefits: list[BenefitSchema]
    coverage_gaps: list[dict] = []
    recommendations: list[str] = []
    confidence: str
    warnings: list[str] = []
