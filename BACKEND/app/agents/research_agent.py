from app.services import llm_router
from app.services.tavily import tavily_service
from loguru import logger


class ResearchAgent:
    async def research(self, query: str, max_results: int = 5, depth: str = "basic") -> str:
        search_results = await tavily_service.search(query, max_results=max_results, search_depth=depth)

        if not search_results:
            return '{"results": [], "answer": null, "summary": "No search results available. Information could not be verified from available sources.", "sources": []}'

        results_text = ""
        for i, r in enumerate(search_results):
            results_text += f"\n[{i+1}] Title: {r['title']}\nContent: {r['content'][:1000]}\nURL: {r['url']}\n"

        prompt = f"""
        Analyze these search results and provide a comprehensive summary.

        USER QUERY: {query}

        SEARCH RESULTS:
        {results_text}

        Return a JSON with:
        {{
            "results": [
                {{
                    "title": "<result title>",
                    "snippet": "<key information>",
                    "url": "<source URL>",
                    "relevance": "<high/medium/low>"
                }}
            ],
            "answer": "<direct answer to the query if possible, or say information could not be verified>",
            "summary": "<concise summary of findings>",
            "key_findings": ["<list of key findings>"],
            "sources": ["<list of source URLs>"],
            "confidence": "<verified if from reliable sources, otherwise needs_review>"
        }}
        """
        return await llm_router.generate(
            system_prompt="You are a thorough researcher. Only report what is found in search results. If information is unavailable, state that clearly.",
            user_prompt=prompt,
            temperature=0.1,
            json_mode=True,
        )

    async def research_policy_trends(self, policy_type: str) -> str:
        query = f"{policy_type} insurance policy trends market benchmarks India 2025 2026"
        results = await tavily_service.search(query, max_results=5, search_depth="advanced")
        return await self._summarize_results(query, results)

    async def research_regulatory(self) -> str:
        results = await tavily_service.search_regulatory_updates()
        return await self._summarize_results("Latest IRDAI regulations and insurance guidelines", results)

    async def _summarize_results(self, query: str, results: list[dict]) -> str:
        if not results:
            return '{"summary": "No information available from current sources.", "confidence": "not_found"}'

        context = "\n".join([f"- {r['title']}: {r['content'][:500]}" for r in results])
        prompt = f"""
        Summarize these research findings about: {query}

        FINDINGS:
        {context}

        Return JSON with summary, key_findings list, sources list, and confidence field.
        """
        return await llm_router.generate(
            system_prompt="Summarize research findings accurately.",
            user_prompt=prompt,
            temperature=0.1,
            json_mode=True,
        )


research_agent = ResearchAgent()
