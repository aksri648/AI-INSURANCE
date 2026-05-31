from app.services import llm_router


class InsuranceEducationAgent:
    async def explain(self, query: str, context: str = "", difficulty: str = "beginner") -> str:
        prompt = f"""
        Explain this insurance topic in simple, clear language.

        USER QUERY: {query}

        RELEVANT CONTEXT:
        {context}
        """
        return await llm_router.generate(
            system_prompt="You are a patient insurance teacher. Explain complex topics simply. Never give personal advice, only educational information.",
            user_prompt=prompt,
            temperature=0.3,
            json_mode=True,
        )


insurance_education_agent = InsuranceEducationAgent()
