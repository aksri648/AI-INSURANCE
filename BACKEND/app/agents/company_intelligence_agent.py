from app.services import llm_router
from app.services.tavily import tavily_service
import json


class CompanyIntelligenceAgent:
    async def analyze_company(self, company_name: str) -> str:
        search_results = await tavily_service.search_insurance_company(company_name)

        search_context = ""
        for r in search_results:
            search_context += f"\nTitle: {r['title']}\nContent: {r['content'][:500]}\nURL: {r['url']}\n"

        prompt = f"""
        Analyze this insurance company based on available data.

        COMPANY NAME: {company_name}

        SEARCH RESULTS:
        {search_context}
        """
        return await llm_router.generate(
            system_prompt="You are an objective insurance company analyst. Only report verified data from search results. Never fabricate company metrics.",
            user_prompt=prompt,
            temperature=0.1,
            json_mode=True,
        )

    async def compare_companies(self, company_names: list[str]) -> str:
        companies_data = []
        for name in company_names:
            result = await self.analyze_company(name)
            try:
                companies_data.append(json.loads(result) if isinstance(result, str) else result)
            except json.JSONDecodeError:
                companies_data.append({"name": name, "error": "Could not analyze"})

        prompt = f"""
        Compare these insurance companies:

        {json.dumps(companies_data, indent=2)}

        Return a JSON with:
        {{
            "comparison": [
                {{
                    "metric": "<metric name>",
                    "companies": {{
                        "<company_name>": "<value>"
                    }}
                }}
            ],
            "best_overall": "<company name>",
            "best_claim_settlement": "<company name>",
            "most_financially_stable": "<company name>",
            "summary": "<comparison summary>",
            "recommendation": "<recommendation based on comparison>"
        }}
        """
        return await llm_router.generate(
            system_prompt="You provide objective company comparisons based solely on available data.",
            user_prompt=prompt,
            temperature=0.1,
            json_mode=True,
        )


company_intelligence_agent = CompanyIntelligenceAgent()
