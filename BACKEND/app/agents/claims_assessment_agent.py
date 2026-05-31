from crewai import Agent
from app.services import llm_router


class ClaimsAssessmentAgent:
    def __init__(self):
        self.agent = Agent(
            role="Claims Assessment Specialist",
            goal="Analyze claim readiness, coverage eligibility, and estimate possible claim payouts",
            backstory="Senior insurance claims adjuster with 20 years experience evaluating claims across all insurance types.",
            verbose=True,
            allow_delegation=False,
        )

    async def assess_claim(
        self, policy_data: dict, benefits: list[dict], claim_type: str, claim_amount: str, description: str
    ) -> str:
        prompt = f"""
        Assess this insurance claim based on the policy details.

        POLICY DATA:
        {policy_data}

        BENEFITS:
        {benefits}

        CLAIM TYPE: {claim_type}
        CLAIM AMOUNT: {claim_amount}
        CLAIM DESCRIPTION: {description}

        Return a JSON with:
        {{
            "eligibility_score": <0-100 number>,
            "estimated_payout": "<estimated amount or range>",
            "assessment": {{
                "covered": <true/false>,
                "applicable_benefits": ["<list of benefits that apply>"],
                "waiting_period_status": "<met/not_met/partial>",
                "exclusion_checks": ["<list of exclusions checked>"],
                "documentation_required": ["<list of required docs>"],
                "conditions_to_meet": ["<list of conditions>"]
            }},
            "coverage_limits": {{
                "sub_limits": ["<any sub-limits that apply>"],
                "deductible": "<deductible amount if any>",
                "copay": "<copay if any>",
                "max_coverage": "<maximum coverage>"
            }},
            "recommendations": ["<list of recommendations>"],
            "risks": ["<list of risk factors>"],
            "summary": "<plain language summary for user>"
        }}

        CRITICAL: Base all estimates strictly on policy data. If information is insufficient, state what is missing.
        """
        return await llm_router.generate(
            system_prompt="You are a precise claims assessor. Only estimate based on available policy data. Never inflate or deflate estimates.",
            user_prompt=prompt,
            temperature=0.1,
            json_mode=True,
        )


claims_assessment_agent = ClaimsAssessmentAgent()
