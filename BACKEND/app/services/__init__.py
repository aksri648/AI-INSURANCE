from app.config import settings
from typing import Optional
import httpx
import json
from tenacity import retry, stop_after_attempt, wait_exponential
from loguru import logger
import numpy as np


class LLMRouter:
    def __init__(self):
        self.groq_api_key = settings.groq_api_key
        self.groq_model = settings.groq_model
        self._embedding_model = None

    def _get_embedding_model(self):
        if self._embedding_model is None:
            try:
                from sentence_transformers import SentenceTransformer
                self._embedding_model = SentenceTransformer("all-MiniLM-L6-v2")
                logger.info("Loaded local embedding model")
            except Exception as e:
                logger.warning(f"Failed to load embedding model: {e}")
        return self._embedding_model

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10))
    async def generate(
        self,
        system_prompt: str,
        user_prompt: str,
        model: Optional[str] = None,
        temperature: float = 0.1,
        json_mode: bool = False,
        max_tokens: int = 4096,
    ) -> str:
        if not self.groq_api_key:
            raise ValueError("No LLM provider configured. Set GROQ_API_KEY.")
        return await self._call_groq(system_prompt, user_prompt, temperature, json_mode, max_tokens)

    async def _call_groq(
        self, system_prompt: str, user_prompt: str, temperature: float, json_mode: bool, max_tokens: int
    ) -> str:
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ]
        payload = {
            "model": self.groq_model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens,
        }
        if json_mode:
            payload["response_format"] = {"type": "json_object"}

        headers = {
            "Authorization": f"Bearer {self.groq_api_key}",
            "Content-Type": "application/json",
        }
        async with httpx.AsyncClient(timeout=120.0) as client:
            response = await client.post("https://api.groq.com/openai/v1/chat/completions", json=payload, headers=headers)
            response.raise_for_status()
            data = response.json()
            return data["choices"][0]["message"]["content"]

    async def generate_embeddings(self, texts: list[str]) -> list[list[float]]:
        model = self._get_embedding_model()
        if model is None:
            logger.error("No embedding model available")
            return [[0.0] * 384 for _ in texts]

        try:
            embeddings = model.encode(texts, show_progress_bar=False)
            return embeddings.tolist() if isinstance(embeddings, np.ndarray) else embeddings
        except Exception as e:
            logger.error(f"Local embedding failed: {e}")
            return [[0.0] * 384 for _ in texts]


llm_router = LLMRouter()
