from pydantic import BaseModel, Field
from typing import Optional
from uuid import UUID


class ChatMessage(BaseModel):
    role: str = Field(..., pattern="^(user|assistant|system)$")
    content: str


class ChatRequest(BaseModel):
    policy_id: UUID
    message: str = Field(..., max_length=5000)
    conversation_history: list[ChatMessage] = []


class ChatResponse(BaseModel):
    reply: str
    sources: list[dict] = []
    confidence: str
    suggested_questions: list[str] = []
