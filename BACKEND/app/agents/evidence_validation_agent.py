from crewai import Agent
from app.services import llm_router
import json


class EvidenceValidationAgent:
    def __init__(self):
        self.agent = Agent(
            role="Evidence Validator",
            goal="Verify that every factual statement from AI agents can be traced to specific source evidence",
            backstory="Expert in fact-checking and evidence verification with background in forensic document analysis.",
            verbose=True,
            allow_delegation=False,
        )

    async def validate(self, claim: str, source_chunks: list[str]) -> dict:
        chunks_text = "\n\n".join([f"[Chunk {i+1}]: {c}" for i, c in enumerate(source_chunks)])

        prompt = f"""
        Validate this claim against the provided source evidence.

        CLAIM: {claim}

        SOURCE EVIDENCE:
        {chunks_text[:8000]}

        Return a JSON with:
        {{
            "is_supported": <true/false/partial>,
            "confidence": "<verified/needs_review/not_found>",
            "supporting_evidence": ["<exact quotes from source that support the claim>"],
            "contradicting_evidence": ["<exact quotes from source that contradict the claim>"],
            "explanation": "<brief explanation of validation result>",
            "missing_elements": ["<parts of claim not found in sources>"]
        }}
        """
        result = await llm_router.generate(
            system_prompt="You are a strict evidence validator. Only verify claims that have clear, direct support in the source evidence.",
            user_prompt=prompt,
            temperature=0.05,
            json_mode=True,
        )
        return json.loads(result) if isinstance(result, str) else result


evidence_validation_agent = EvidenceValidationAgent()
