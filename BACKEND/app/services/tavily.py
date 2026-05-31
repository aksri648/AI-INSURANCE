from app.config import settings
from typing import Optional
import httpx
from loguru import logger


class TavilyService:
    def __init__(self):
        self.api_key = settings.tavily_api_key
        self.base_url = "https://api.tavily.com"

    async def search(self, query: str, max_results: int = 5, search_depth: str = "basic") -> list[dict]:
        if not self.api_key:
            logger.warning("Tavily API key not configured")
            return []

        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.post(
                    f"{self.base_url}/search",
                    json={
                        "api_key": self.api_key,
                        "query": query,
                        "max_results": max_results,
                        "search_depth": search_depth,
                        "include_answer": True,
                        "include_raw_content": False,
                    },
                )
                response.raise_for_status()
                data = response.json()

                results = []
                for r in data.get("results", []):
                    results.append({
                        "title": r.get("title", ""),
                        "url": r.get("url", ""),
                        "content": r.get("content", ""),
                        "score": r.get("score", 0.0),
                    })

                logger.info(f"Tavily search returned {len(results)} results for: {query[:50]}")
                return results

        except Exception as e:
            logger.error(f"Tavily search failed: {e}")
            return []

    async def search_insurance_company(self, company_name: str) -> list[dict]:
        query = f"{company_name} insurance company claim settlement ratio IRDAI report 2024 2025"
        return await self.search(query, max_results=5, search_depth="advanced")

    async def search_regulatory_updates(self) -> list[dict]:
        query = "IRDAI latest regulations insurance guidelines 2025 2026"
        return await self.search(query, max_results=5, search_depth="advanced")

    async def search_policy_benchmarks(self, policy_type: str) -> list[dict]:
        query = f"{policy_type} insurance policy benchmark coverage comparison India 2025"
        return await self.search(query, max_results=5, search_depth="basic")


tavily_service = TavilyService()
