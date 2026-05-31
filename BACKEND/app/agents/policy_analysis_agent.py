from app.services import llm_router


class PolicyAnalysisAgent:
    async def analyze_policy(self, extracted_text: str) -> str:
        prompt = f"""
        Analyze this insurance policy document and extract ALL structured information.
        Return a JSON object with these fields:
        {{
            "policy_type": "<health/life/motor/home/travel/general>",
            "insurer": "<company name>",
            "policy_number": "<policy number if found>",
            "summary": "<2-3 sentence summary in simple language>",
            "benefits": [
                {{
                    "name": "<benefit name>",
                    "description": "<simple explanation>",
                    "coverage_amount": "<amount or range>",
                    "currency": "INR",
                    "waiting_period": "<waiting period if any, else 'None'>",
                    "exclusions": "<specific exclusions for this benefit>",
                    "conditions": "<conditions to claim>",
                    "claim_limit": "<limit if any>",
                    "deductible": "<deductible if any>",
                    "copay": "<copay if any>",
                    "is_sub_limit": false,
                    "parent_benefit": "<if this is a sub-limit of another benefit>"
                }}
            ],
            "exclusions": ["<list of all exclusions>"],
            "waiting_periods": [{{"benefit": "<name>", "period": "<duration>"}}],
            "premium": "<amount if found>",
            "coverage_end_date": "<date if found>",
            "policy_terms": ["<key terms>"],
            "hidden_clauses": ["<potentially unfavorable clauses>"]
        }}

        CRITICAL: Only extract information explicitly stated in the document. If something is not found, use null or empty array. Never invent policy details.

        DOCUMENT TEXT:
        {extracted_text[:15000]}
        """
        return await llm_router.generate(
            system_prompt="You are a precise insurance policy analyst. Extract every detail accurately from the provided document text. Never hallucinate.",
            user_prompt=prompt,
            temperature=0.05,
            json_mode=True,
        )


policy_analysis_agent = PolicyAnalysisAgent()
