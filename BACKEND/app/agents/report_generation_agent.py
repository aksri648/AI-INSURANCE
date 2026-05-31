from app.services import llm_router
from app.services.report_engine import report_engine
import json


class ReportGenerationAgent:
    async def generate_report(self, analysis_data: dict) -> str:
        prompt = f"""
        Generate a comprehensive insurance analysis report JSON that will be rendered as HTML.

        ANALYSIS DATA:
        {analysis_data}

        Return a JSON with these sections:
        {{
            "title": "<report title>",
            "subtitle": "<report subtitle>",
            "generated_at": "<timestamp>",
            "summary": {{
                "overview": "<2-3 sentence overview in simple language>",
                "total_benefits": <count>,
                "total_coverage": "<total coverage amount>",
                "claim_score": "<score>/10",
                "confidence": "<verified/needs_review>"
            }},
            "benefits": [<list of benefit objects with name, description, coverage_amount, confidence>],
            "coverage_items": [<list of coverage items with benefit, covered, amount, waiting_period, conditions, status, source>],
            "exclusions": ["<list of exclusions in simple language>"],
            "waiting_periods": [{{"benefit": "<name>", "period": "<duration>"}}],
            "hidden_conditions": [{{"title": "<title>", "description": "<description>", "severity": "<high/medium/low>"}}],
            "claim_score": {{
                "score": "<score>",
                "ease": "<score>",
                "documentation": "<score>",
                "explanation": "<explanation>"
            }},
            "coverage_adequacy": {{
                "rating": "<rating>/10",
                "analysis": "<analysis>",
                "gaps": ["<list of gaps>"]
            }},
            "suggestions": [{{"title": "<title>", "description": "<description>"}}],
            "mis_selling": {{
                "findings": [{{"title": "<title>", "description": "<description>", "severity": "<severity>"}}],
                "severity": "<severity>",
                "summary": "<summary>"
            }},
            "claim_scenarios": [{{"title": "<title>", "description": "<description>", "estimated_payout": "<amount>", "likelihood": "<likelihood>"}}],
            "trust_score": {{
                "score": "<score>",
                "claim_ratio": "<percentage>",
                "solvency": "<percentage>",
                "explanation": "<explanation>"
            }},
            "sources": [{{"title": "<source title>", "description": "<description>", "confidence": "<confidence>"}}],
            "verdict": {{
                "rating": "<rating>/10",
                "summary": "<final summary>",
                "pros": ["<list of pros>"],
                "cons": ["<list of cons>"]
            }}
        }}
        """
        json_result = await llm_router.generate(
            system_prompt="You generate comprehensive, evidence-based insurance report data. Every claim must be supported by evidence.",
            user_prompt=prompt,
            temperature=0.2,
            json_mode=True,
        )

        data = json.loads(json_result) if isinstance(json_result, str) else json_result
        return report_engine.generate_full_report(data)


report_generation_agent = ReportGenerationAgent()
