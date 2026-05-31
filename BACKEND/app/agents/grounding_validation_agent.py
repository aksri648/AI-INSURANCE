from crewai import Agent
from app.services import llm_router
import json


class GroundingValidationAgent:
    def __init__(self):
        self.agent = Agent(
            role="Grounding Validator",
            goal="Ensure every statement in the final report has proper citations and verifiable sources",
            backstory="Quality assurance specialist ensuring all AI-generated content meets strict evidence standards.",
            verbose=True,
            allow_delegation=False,
        )

    async def validate_report(self, report_sections: dict, available_sources: list[str]) -> dict:
        sources_text = "\n".join([f"- {s}" for s in available_sources])

        prompt = f"""
        Validate that every statement in the report sections is properly grounded in available sources.

        REPORT SECTIONS:
        {report_sections}

        AVAILABLE SOURCES:
        {sources_text}

        Return a JSON with:
        {{
            "overall_score": <0-100>,
            "is_pass": <true/false>,
            "section_scores": {{
                "<section_name>": {{
                    "score": <0-100>,
                    "issues": ["<list of ungrounded statements>"],
                    "status": "<pass/fail/warning>"
                }}
            }},
            "ungrounded_statements": [
                {{
                    "statement": "<the ungrounded statement>",
                    "section": "<which section>",
                    "suggestion": "<how to ground it>"
                }}
            ],
            "summary": "<overall assessment>"
        }}

        CRITICAL: Flag any statement that cannot be directly traced to a source. Confidence indicators must be accurate.
        """
        result = await llm_router.generate(
            system_prompt="You are a strict grounding validator. Any statement without a clear source must be flagged. Do not pass ungrounded content.",
            user_prompt=prompt,
            temperature=0.05,
            json_mode=True,
        )
        return json.loads(result) if isinstance(result, str) else result


grounding_validation_agent = GroundingValidationAgent()
