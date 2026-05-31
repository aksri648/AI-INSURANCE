from app.config import settings
from typing import Optional, AsyncGenerator
import httpx
import json
from tenacity import retry, stop_after_attempt, wait_exponential
from loguru import logger


class LLMRouter:
    def __init__(self):
        self.ollama_base = settings.ollama_base_url
        self.primary_model = settings.ollama_primary_model
        self.fallback_model = settings.ollama_fallback_model
        self.groq_api_key = settings.groq_api_key
        self.groq_model = settings.groq_model
        self.use_groq_fallback = settings.groq_fallback

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
        model = model or self.primary_model
        try:
            return await self._call_ollama(system_prompt, user_prompt, model, temperature, json_mode, max_tokens)
        except Exception as e:
            logger.warning(f"Ollama primary failed: {e}. Trying fallback.")
            try:
                return await self._call_ollama(system_prompt, user_prompt, self.fallback_model, temperature, json_mode, max_tokens)
            except Exception as e2:
                logger.warning(f"Ollama fallback failed: {e2}.")
                if self.use_groq_fallback and self.groq_api_key:
                    return await self._call_groq(system_prompt, user_prompt, temperature, json_mode, max_tokens)
                raise

    async def _call_ollama(
        self, system_prompt: str, user_prompt: str, model: str, temperature: float, json_mode: bool, max_tokens: int
    ) -> str:
        payload = {
            "model": model,
            "system": system_prompt,
            "prompt": user_prompt,
            "temperature": temperature,
            "stream": False,
            "options": {"num_predict": max_tokens},
        }
        if json_mode:
            payload["format"] = "json"

        async with httpx.AsyncClient(timeout=120.0) as client:
            response = await client.post(f"{self.ollama_base}/api/generate", json=payload)
            response.raise_for_status()
            data = response.json()
            return data.get("response", "")

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

    async def generate_embeddings(self, texts: list[str], model: Optional[str] = None) -> list[list[float]]:
        model = model or settings.ollama_embedding_model
        try:
            async with httpx.AsyncClient(timeout=60.0) as client:
                response = await client.post(
                    f"{self.ollama_base}/api/embed",
                    json={"model": model, "input": texts},
                )
                response.raise_for_status()
                data = response.json()
                return data.get("embeddings", [])
        except Exception as e:
            logger.error(f"Embedding generation failed: {e}")
            raise


llm_router = LLMRouter()
