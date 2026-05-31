from app.services import llm_router


class RecommendationAgent:
    async def generate_recommendations(self, user_profile: dict, policies: list[dict]) -> str:
        profile_str = "\n".join(f"{k}: {v}" for k, v in user_profile.items())
        policies_str = ""
        for p in policies:
            policies_str += f"- {p.get('title', 'Unknown')} ({p.get('policy_type', 'N/A')}): {p.get('summary', '')[:200]}\n"

        prompt = f"""
        Based on this user profile and their existing insurance policies, provide personalized recommendations.

        USER PROFILE:
        {profile_str}

        EXISTING POLICIES:
        {policies_str}

        Return a JSON with:
        {{
            "recommendations": [
                {{
                    "type": "<gap_filling/upgrade/new_coverage/risk_mitigation>",
                    "priority": "<high/medium/low>",
                    "title": "<clear title>",
                    "description": "<simple explanation of recommendation>",
                    "reasoning": "<why this is recommended>",
                    "category": "<health/life/motor/home/travel/investment>"
                }}
            ],
            "coverage_gaps": ["<list of identified gaps>"],
            "risk_factors": ["<list of risk factors>"],
            "summary": "<overall assessment>"
        }}
        """
        return await llm_router.generate(
            system_prompt="You are a responsible insurance advisor. Only recommend what is appropriate based on evidence. Never recommend products without clear reasoning.",
            user_prompt=prompt,
            temperature=0.2,
            json_mode=True,
        )


recommendation_agent = RecommendationAgent()
