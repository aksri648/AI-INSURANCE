from app.services import llm_router
import json


class EvidenceValidationAgent:
    async def validate(self, claim: str, source_chunks: list[str]) -> dict:
        chunks_text = "\n\n".join([f"[Chunk {i+1}]: {c}" for i, c in enumerate(source_chunks)])

        prompt = f"""
        Validate this claim against the provided source evidence.

        CLAIM: {claim}

        SOURCE EVIDENCE:
        {chunks_text}
        """
        result = await llm_router.generate(
            system_prompt="You are a strict evidence validator. Only verify claims that have clear, direct support in the source evidence.",
            user_prompt=prompt,
            temperature=0.05,
            json_mode=True,
        )
        return json.loads(result) if isinstance(result, str) else result


evidence_validation_agent = EvidenceValidationAgent()
