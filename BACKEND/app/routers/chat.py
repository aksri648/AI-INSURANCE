from fastapi import APIRouter, Depends, HTTPException
from app.middleware.clerk import get_current_user
from app.models import User, Policy, PolicyChunk
from app.database import async_session
from app.schemas.chat import ChatRequest, ChatResponse
from app.services.rag import rag_service
from app.services import llm_router
from sqlalchemy import select
from sqlalchemy.orm import selectinload
import json
from loguru import logger

router = APIRouter(prefix="/api/chat", tags=["Chat"])


@router.post("/policy/{policy_id}", response_model=ChatResponse)
async def chat_with_policy(
    policy_id: str,
    request: ChatRequest,
    user: User = Depends(get_current_user),
):
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

    relevant_chunks = await rag_service.retrieve_relevant_chunks(policy_id, request.message)
    context = rag_service.build_context(relevant_chunks)

    policy_context = f"""
Policy Title: {policy.title}
Insurer: {policy.insurer or 'N/A'}
Type: {policy.policy_type}
Summary: {policy.summary or 'N/A'}
"""

    benefits_context = ""
    if policy.benefits:
        benefits_context = "\nBenefits:\n" + "\n".join(
            f"- {b.name}: {b.coverage_amount or 'N/A'} (Waiting: {b.waiting_period or 'None'})"
            for b in policy.benefits
        )

    history_text = ""
    for msg in request.conversation_history[-10:]:
        history_text += f"\n{msg.role}: {msg.content}"

    system_prompt = """You are Insurance Copilot, an evidence-based insurance intelligence system. Your ONLY source of truth is the provided policy document context.

RULES:
1. NEVER make up benefits, coverage amounts, waiting periods, or exclusions
2. If the answer is not in the provided context, say "This information could not be found in your policy document. Please check your policy document or contact your insurer."
3. Always cite specific sections from the document
4. Use simple language (8th grade reading level)
5. If asked about something ambiguous, ask clarifying questions
6. Mark confidence: 🟢 Verified (found in docs), 🟡 Needs Review (partial info), 🔴 Not Found (no evidence)"""

    user_prompt = f"""
POLICY CONTEXT:
{policy_context}

BENEFITS:
{benefits_context}

DOCUMENT EXCERPTS:
{context}

CONVERSATION HISTORY:
{history_text}

USER QUESTION: {request.message}

Provide a helpful, evidence-based answer. If the information is in the policy, cite the specific document section. If not, say so clearly."""

    try:
        reply = await llm_router.generate(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            temperature=0.1,
        )

        suggested = [
            "What benefits am I covered for?",
            "What is the waiting period for pre-existing conditions?",
            "How much coverage do I have?",
            "What are the exclusions?",
            "Can you explain the claim process?",
        ]

        return ChatResponse(
            reply=reply,
            sources=[{"title": f"Document {c['chunk_index']}", "content": c["content"][:200]} for c in relevant_chunks[:3]],
            confidence="verified" if relevant_chunks else "needs_review",
            suggested_questions=suggested,
        )

    except Exception as e:
        logger.error(f"Chat failed: {e}")
        raise HTTPException(status_code=500, detail="Failed to generate response")
