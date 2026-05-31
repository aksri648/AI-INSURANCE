from app.services import llm_router
from app.config import settings
from typing import Optional
from loguru import logger


class EmbeddingService:
    def __init__(self):
        self.dimension = settings.pgvector_dimension

    async def embed_text(self, text: str) -> list[float]:
        embeddings = await llm_router.generate_embeddings([text])
        if embeddings:
            return embeddings[0]
        return [0.0] * self.dimension

    async def embed_texts(self, texts: list[str]) -> list[list[float]]:
        if not texts:
            return []
        batch_size = 10
        all_embeddings = []
        for i in range(0, len(texts), batch_size):
            batch = texts[i : i + batch_size]
            embeddings = await llm_router.generate_embeddings(batch)
            all_embeddings.extend(embeddings)
            logger.debug(f"Embedded batch {i // batch_size + 1}/{(len(texts) - 1) // batch_size + 1}")
        return all_embeddings

    async def embed_chunks(self, chunks: list[dict]) -> list[dict]:
        texts = [c["content"] for c in chunks]
        embeddings = await self.embed_texts(texts)
        for chunk, embedding in zip(chunks, embeddings):
            chunk["embedding"] = embedding
        return chunks


embedding_service = EmbeddingService()
