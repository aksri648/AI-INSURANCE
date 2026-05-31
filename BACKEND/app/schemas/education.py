from pydantic import BaseModel, Field
from typing import Optional


class EducationQuery(BaseModel):
    query: str = Field(..., max_length=1000)
    difficulty: str = "beginner"


class EducationResponse(BaseModel):
    topic: str
    explanation: str
    key_takeaways: list[str] = []
    related_topics: list[str] = []
    sources: list[dict] = []
    confidence: str


class MisSellingCheckRequest(BaseModel):
    policy_id: str
    specific_concern: Optional[str] = None


class MisSellingCheckResponse(BaseModel):
    findings: list[dict] = []
    severity: str
    summary: str
    recommendations: list[str] = []
    evidence_refs: list[dict] = []
    confidence: str
