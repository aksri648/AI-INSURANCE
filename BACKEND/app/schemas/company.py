from pydantic import BaseModel, Field
from typing import Optional


class CompanySearchRequest(BaseModel):
    company_name: str = Field(..., max_length=500)


class CompanyResponse(BaseModel):
    id: Optional[str] = None
    name: str
    irda_id: Optional[str] = None
    website: Optional[str] = None
    description: Optional[str] = None
    claim_settlement_ratio: Optional[float] = None
    solvency_ratio: Optional[float] = None
    market_share: Optional[float] = None
    complaints_summary: Optional[str] = None
    ratings: dict = {}
    irda_compliance: Optional[str] = None
    trust_score: Optional[float] = None
    confidence: str
    sources: list[str] = []


class CompanyCompareRequest(BaseModel):
    company_names: list[str] = Field(..., min_length=2, max_length=5)
