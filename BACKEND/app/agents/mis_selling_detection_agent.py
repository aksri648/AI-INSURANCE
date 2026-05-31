from app.services import llm_router


class MisSellingDetectionAgent:
    async def detect_mis_selling(self, policy_data: dict, extracted_text: str) -> str:
        prompt = f"""
        Analyze this insurance policy for potential mis-selling, misleading statements, hidden clauses, and unfair terms.

        POLICY DATA:
        {policy_data}

        DOCUMENT TEXT:
        {extracted_text}
        """
        return await llm_router.generate(
            system_prompt="You are an objective insurance mis-selling investigator. Only flag issues with clear evidence. Do not exaggerate findings.",
            user_prompt=prompt,
            temperature=0.05,
            json_mode=True,
        )


mis_selling_detection_agent = MisSellingDetectionAgent()
