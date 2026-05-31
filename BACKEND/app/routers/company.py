from fastapi import APIRouter, Depends, HTTPException
from app.middleware.clerk import get_current_user
from app.models import User, Company
from app.database import async_session
from app.schemas.company import CompanySearchRequest, CompanyResponse, CompanyCompareRequest
from app.agents.company_intelligence_agent import company_intelligence_agent
from sqlalchemy import select
import json
from loguru import logger

router = APIRouter(prefix="/api/companies", tags=["Company Intelligence"])


@router.post("/search", response_model=CompanyResponse)
async def search_company(
    request: CompanySearchRequest,
    user: User = Depends(get_current_user),
):
    async with async_session() as session:
        stmt = select(Company).where(Company.name.ilike(f"%{request.company_name}%"))
        result = await session.execute(stmt)
        existing = result.scalar_one_or_none()

    if existing and existing.metadata.get("last_updated_days", 99) < 7:
        return _company_to_response(existing)

    try:
        result_text = await company_intelligence_agent.analyze_company(request.company_name)
        data = json.loads(result_text) if isinstance(result_text, str) else result_text

        async with async_session() as session:
            company = existing or Company(name=data.get("name", request.company_name))
            company.irda_id = data.get("irda_id", company.irda_id)
            company.website = data.get("website", company.website)
            company.description = data.get("description", company.description)
            company.claim_settlement_ratio = data.get("claim_settlement_ratio", company.claim_settlement_ratio)
            company.solvency_ratio = data.get("solvency_ratio", company.solvency_ratio)
            company.market_share = data.get("market_share", company.market_share)
            company.ratings = data.get("ratings", company.ratings or {})
            company.irda_compliance = data.get("irda_compliance", company.irda_compliance)
            company.metadata = {**company.metadata, "sources": data.get("sources", []), "last_updated_days": 0}

            if not existing:
                session.add(company)
            await session.commit()
            await session.refresh(company)

        return CompanyResponse(
            id=str(company.id),
            name=company.name,
            irda_id=company.irda_id,
            website=company.website,
            description=company.description,
            claim_settlement_ratio=company.claim_settlement_ratio,
            solvency_ratio=company.solvency_ratio,
            market_share=company.market_share,
            complaints_summary=data.get("complaints_summary"),
            ratings=data.get("ratings", {}),
            irda_compliance=company.irda_compliance,
            trust_score=data.get("trust_score"),
            confidence="verified" if data.get("claim_settlement_ratio") else "needs_review",
            sources=data.get("sources", []),
        )

    except Exception as e:
        logger.error(f"Company search failed: {e}")
        raise HTTPException(status_code=500, detail=f"Search failed: {str(e)}")


@router.post("/compare")
async def compare_companies(
    request: CompanyCompareRequest,
    user: User = Depends(get_current_user),
):
    try:
        result_text = await company_intelligence_agent.compare_companies(request.company_names)
        data = json.loads(result_text) if isinstance(result_text, str) else result_text
        return data
    except Exception as e:
        logger.error(f"Company comparison failed: {e}")
        raise HTTPException(status_code=500, detail=f"Comparison failed: {str(e)}")


def _company_to_response(company: Company) -> CompanyResponse:
    return CompanyResponse(
        id=str(company.id),
        name=company.name,
        irda_id=company.irda_id,
        website=company.website,
        description=company.description,
        claim_settlement_ratio=company.claim_settlement_ratio,
        solvency_ratio=company.solvency_ratio,
        market_share=company.market_share,
        complaints_summary=(company.complaints_data or {}).get("summary"),
        ratings=company.ratings or {},
        irda_compliance=company.irda_compliance,
        trust_score=None,
        confidence="verified",
        sources=(company.metadata or {}).get("sources", []),
    )
