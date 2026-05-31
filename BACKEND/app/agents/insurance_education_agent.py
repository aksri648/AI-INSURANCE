from crewai import Agent
from app.services import llm_router


class InsuranceEducationAgent:
    def __init__(self):
        self.agent = Agent(
            role="Insurance Education Specialist",
            goal="Explain insurance concepts in simple, clear language that anyone can understand",
            backstory="Experienced insurance educator who has taught thousands of people to understand their insurance policies and make informed decisions.",
            verbose=True,
            allow_delegation=False,
        )

    async def explain(self, query: str, context: str = "", difficulty: str = "beginner") -> str:
        prompt = f"""
        Explain this insurance topic in simple, clear language.

        USER QUERY: {query}

        RELEVANT CONTEXT:
        {context[:5000]}

        Difficulty level: {difficulty}

        Return a JSON with:
        {{
            "topic": "<the main topic>",
            "explanation": "<thorough but simple explanation, use analogies and examples>",
            "key_takeaways": ["<3-5 key points to remember>"],
            "related_topics": ["<related topics user might want to learn>"],
            "definitions": {{
                "<term>": "<simple definition>"
            }}
        }}

        RULES:
        - Use 8th-grade reading level
        - Avoid jargon unless explained
        - Use real-world examples
        - Use analogies from daily life
        - Keep paragraphs short (2-3 sentences max)
        """
        return await llm_router.generate(
            system_prompt="You are a patient insurance teacher. Explain complex topics simply. Never give personal advice, only educational information.",
            user_prompt=prompt,
            temperature=0.3,
            json_mode=True,
        )


insurance_education_agent = InsuranceEducationAgent()
