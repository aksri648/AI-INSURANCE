from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from app.middleware.clerk import get_current_user
from app.models import User, Policy, PolicyChunk, Benefit
from app.database import async_session
from app.schemas.policy import PolicyResponse, PolicyAnalysisResponse, BenefitSchema
from app.services.storage import storage
from app.services.ocr import ocr_service
from app.services.rag import rag_service
from app.services.embedding import embedding_service
from app.agents.policy_analysis_agent import policy_analysis_agent
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from typing import Optional
import json
from loguru import logger

router = APIRouter(prefix="/api/policies", tags=["Policies"])


@router.post("/upload", response_model=PolicyResponse)
async def upload_policy(
    file: UploadFile = File(...),
    title: str = Form(...),
    insurer: Optional[str] = Form(None),
    policy_number: Optional[str] = Form(None),
    policy_type: str = Form("general"),
    user: User = Depends(get_current_user),
):
    ext = file.filename.split(".")[-1].lower() if file.filename else ""
    if ext not in ("pdf", "png", "jpg", "jpeg", "tiff"):
        raise HTTPException(status_code=400, detail=f"Unsupported file type: .{ext}")

    file_path = await storage.save(file.file, file.filename)

    policy = Policy(
        user_id=user.id,
        title=title,
        insurer=insurer,
        policy_number=policy_number,
        policy_type=policy_type,
        file_path=file_path,
        file_type=ext,
    )

    try:
        extracted_text = await ocr_service.extract_text(file_path, ext)
        metadata = await ocr_service.extract_metadata(file_path)

        policy.extracted_text = extracted_text
        policy.page_count = metadata.get("page_count", 0)
        policy.file_size_bytes = metadata.get("file_size", 0)

        chunks = rag_service.chunk_text(extracted_text, {"policy_title": title})
        chunks = await embedding_service.embed_chunks(chunks)

        async with async_session() as session:
            session.add(policy)
            await session.flush()

            for chunk_data in chunks:
                chunk = PolicyChunk(
                    policy_id=policy.id,
                    chunk_index=chunk_data["chunk_index"],
                    content=chunk_data["content"],
                    embedding=chunk_data.get("embedding"),
                    chunk_metadata=chunk_data.get("metadata", {}),
                )
                session.add(chunk)

            await session.commit()
            await session.refresh(policy)

        return _policy_to_response(policy)

    except Exception as e:
        logger.error(f"Policy upload failed: {e}")
        await storage.delete(file_path)
        raise HTTPException(status_code=500, detail=f"Failed to process policy: {str(e)}")


@router.get("/", response_model=list[PolicyResponse])
async def list_policies(
    page: int = 1,
    page_size: int = 20,
    user: User = Depends(get_current_user),
):
    offset = (page - 1) * page_size
    async with async_session() as session:
        stmt = (
            select(Policy)
            .where(Policy.user_id == user.id, Policy.is_active == True)
            .options(selectinload(Policy.benefits))
            .order_by(Policy.created_at.desc())
            .offset(offset)
            .limit(page_size)
        )
        result = await session.execute(stmt)
        policies = result.scalars().all()
        return [_policy_to_response(p) for p in policies]


@router.get("/{policy_id}", response_model=PolicyResponse)
async def get_policy(policy_id: str, user: User = Depends(get_current_user)):
    async with async_session() as session:
        stmt = (
            select(Policy)
            .where(Policy.id == policy_id, Policy.user_id == user.id, Policy.is_active == True)
            .options(selectinload(Policy.benefits))
        )
        result = await session.execute(stmt)
        policy = result.scalar_one_or_none()
        if not policy:
            raise HTTPException(status_code=404, detail="Policy not found")
        return _policy_to_response(policy)


@router.post("/{policy_id}/analyze", response_model=PolicyAnalysisResponse)
async def analyze_policy(policy_id: str, user: User = Depends(get_current_user)):
    async with async_session() as session:
        stmt = (
            select(Policy)
            .where(Policy.id == policy_id, Policy.user_id == user.id)
            .options(selectinload(Policy.benefits))
        )
        result = await session.execute(stmt)
        policy = result.scalar_one_or_none()
        if not policy:
            raise HTTPException(status_code=404, detail="Policy not found")

    try:
        analysis_text = await policy_analysis_agent.analyze_policy(policy.extracted_text or "")
        analysis = json.loads(analysis_text) if isinstance(analysis_text, str) else analysis_text

        async with async_session() as session:
            db_policy = await session.get(Policy, policy.id)
            db_policy.structured_data = analysis
            db_policy.summary = analysis.get("summary", "")
            db_policy.policy_type = analysis.get("policy_type", db_policy.policy_type)
            db_policy.status = "analyzed"

            for b in analysis.get("benefits", []):
                if b.get("name"):
                    benefit = Benefit(
                        policy_id=policy.id,
                        name=b["name"],
                        description=b.get("description"),
                        coverage_amount=b.get("coverage_amount"),
                        currency=b.get("currency", "INR"),
                        waiting_period=b.get("waiting_period"),
                        exclusions=b.get("exclusions"),
                        conditions=b.get("conditions"),
                        claim_limit=b.get("claim_limit"),
                        deductible=b.get("deductible"),
                        copay=b.get("copay"),
                        is_sub_limit=b.get("is_sub_limit", False),
                        parent_benefit=b.get("parent_benefit"),
                    )
                    session.add(benefit)

            await session.commit()

        return PolicyAnalysisResponse(
            policy_id=policy.id,
            summary=analysis.get("summary", ""),
            benefits=[BenefitSchema(**b) for b in analysis.get("benefits", []) if b.get("name")],
            coverage_gaps=analysis.get("coverage_gaps", []),
            recommendations=analysis.get("recommendations", []),
            confidence="verified",
            warnings=analysis.get("hidden_clauses", []),
        )

    except Exception as e:
        logger.error(f"Policy analysis failed: {e}")
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")


@router.delete("/{policy_id}")
async def delete_policy(policy_id: str, user: User = Depends(get_current_user)):
    async with async_session() as session:
        stmt = select(Policy).where(Policy.id == policy_id, Policy.user_id == user.id)
        result = await session.execute(stmt)
        policy = result.scalar_one_or_none()
        if not policy:
            raise HTTPException(status_code=404, detail="Policy not found")

        if policy.file_path:
            await storage.delete(policy.file_path)

        policy.is_active = False
        await session.commit()

    return {"message": "Policy deleted"}


def _policy_to_response(policy) -> PolicyResponse:
    return PolicyResponse(
        id=policy.id,
        title=policy.title,
        insurer=policy.insurer,
        policy_number=policy.policy_number,
        policy_type=policy.policy_type.value if hasattr(policy.policy_type, "value") else str(policy.policy_type),
        status=policy.status.value if hasattr(policy.status, "value") else str(policy.status),
        file_type=policy.file_type,
        file_size_bytes=policy.file_size_bytes,
        summary=policy.summary,
        page_count=policy.page_count,
        created_at=policy.created_at,
        updated_at=policy.updated_at,
        benefits=[BenefitSchema.from_orm(b) for b in (policy.benefits or [])],
        structured_data=policy.structured_data or {},
    )
