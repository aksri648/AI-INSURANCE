from app.database import async_session
from app.models import PolicyChunk
from app.config import settings
from sqlalchemy import select, text
from typing import Optional
from loguru import logger
import tiktoken


class RAGService:
    def __init__(self):
        self.chunk_size = settings.chunk_size
        self.chunk_overlap = settings.chunk_overlap
        self.top_k = settings.top_k_retrieval
        try:
            self.tokenizer = tiktoken.get_encoding("cl100k_base")
        except Exception:
            self.tokenizer = None

    def chunk_text(self, text: str, metadata: Optional[dict] = None) -> list[dict]:
        if not text:
            return []

        if self.tokenizer:
            tokens = self.tokenizer.encode(text)
            total_tokens = len(tokens)
        else:
            total_tokens = len(text)

        if total_tokens <= self.chunk_size:
            return [{"content": text, "metadata": metadata or {}, "chunk_index": 0}]

        chunks = []
        start = 0
        index = 0

        while start < total_tokens:
            if self.tokenizer:
                end = min(start + self.chunk_size, total_tokens)
                chunk_tokens = tokens[start:end]
                chunk_text = self.tokenizer.decode(chunk_tokens)
            else:
                end = min(start + self.chunk_size, total_tokens)
                chunk_text = text[start:end]

            chunks.append({
                "content": chunk_text,
                "metadata": metadata or {},
                "chunk_index": index,
            })

            start += self.chunk_size - self.chunk_overlap
            index += 1

        logger.info(f"Split text into {len(chunks)} chunks")
        return chunks

    async def retrieve_relevant_chunks(
        self, policy_id: str, query: str, top_k: Optional[int] = None
    ) -> list[dict]:
        k = top_k or self.top_k
        query_embedding = await self._get_query_embedding(query)

        async with async_session() as session:
            stmt = (
                select(PolicyChunk)
                .where(PolicyChunk.policy_id == policy_id)
                .where(PolicyChunk.embedding.isnot(None))
                .order_by(PolicyChunk.embedding.cosine_distance(query_embedding))
                .limit(k)
            )
            result = await session.execute(stmt)
            chunks = result.scalars().all()

            return [
                {
                    "id": str(c.id),
                    "content": c.content,
                    "chunk_index": c.chunk_index,
                    "metadata": c.metadata or {},
                    "score": 0.0,
                }
                for c in chunks
            ]

    async def _get_query_embedding(self, query: str) -> list[float]:
        from app.services.embedding import embedding_service
        return await embedding_service.embed_text(query)

    def build_context(self, chunks: list[dict]) -> str:
        if not chunks:
            return ""
        parts = []
        for i, chunk in enumerate(chunks):
            parts.append(f"[Document {i + 1}]:\n{chunk['content']}\n")
        return "\n---\n".join(parts)


rag_service = RAGService()
