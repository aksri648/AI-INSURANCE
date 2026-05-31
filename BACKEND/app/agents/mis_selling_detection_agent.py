from crewai import Agent
from app.services import llm_router


class MisSellingDetectionAgent:
    def __init__(self):
        self.agent = Agent(
            role="Insurance Mis-Selling Investigator",
            goal="Detect contradictions, misleading statements, hidden clauses, and potential mis-selling in insurance policies",
            backstory="Former insurance ombudsman investigator specialized in detecting unfair practices, hidden terms, and mis-selling in insurance products.",
            verbose=True,
            allow_delegation=False,
        )

    async def detect_mis_selling(self, policy_data: dict, extracted_text: str) -> str:
        prompt = f"""
        Analyze this insurance policy for potential mis-selling, misleading statements, hidden clauses, and unfair terms.

        POLICY DATA:
        {policy_data}

        DOCUMENT TEXT:
        {extracted_text[:10000]}

        Return a JSON with:
        {{
            "findings": [
                {{
                    "type": "<misleading_statement/hidden_clause/unfair_term/contradiction/exaggerated_benefit>",
                    "severity": "<critical/high/medium/low>",
                    "title": "<short title>",
                    "description": "<detailed finding in simple language>",
                    "evidence": "<exact text from document that supports this finding>",
                    "recommendation": "<what user should do>"
                }}
            ],
            "severity": "<overall severity: critical/high/medium/low>",
            "summary": "<overall summary in simple language>",
            "red_flags": ["<list of red flags>"],
            "user_actions": ["<list of recommended actions for user>"]
        }}

        CRITICAL: Every finding MUST be supported by evidence from the document. If no mis-selling is found, return empty findings array.
        """
        return await llm_router.generate(
            system_prompt="You are an objective insurance mis-selling investigator. Only flag issues with clear evidence. Do not exaggerate findings.",
            user_prompt=prompt,
            temperature=0.05,
            json_mode=True,
        )


mis_selling_detection_agent = MisSellingDetectionAgent()
