import os
from ..data.catalog import PREREQS

async def coach_answer(question: str, profile: dict, roadmap: list):
    api_key = os.getenv("OPENAI_API_KEY")
    if api_key:
        try:
            from openai import AsyncOpenAI
            client = AsyncOpenAI(api_key=api_key)
            context = {
                "role": profile.get("role"),
                "skills": profile.get("skills", {}),
                "hours_per_day": profile.get("hours_per_day"),
                "months": profile.get("months"),
                "roadmap": roadmap[:8]
            }
            resp = await client.chat.completions.create(
                model=os.getenv("OPENAI_MODEL","gpt-4.1-mini"),
                temperature=0.2,
                messages=[
                    {"role":"system","content":"You are LearnPath AI Coach. Answer only from the supplied learner context. Explain recommendations, gaps and tradeoffs. Be concise and actionable."},
                    {"role":"user","content":f"Learner context: {context}\\nQuestion: {question}"}
                ],
            )
            return resp.choices[0].message.content
        except Exception:
            pass

    q = question.lower()
    current = roadmap[0] if roadmap else None
    if "why" in q and current:
        return f"{current['skill']} is next because {', '.join(current['reasons'][:3])}. Its prerequisites are {', '.join(current.get('prerequisites') or ['none'])}."
    if "skip" in q and current:
        score = profile.get("skills",{}).get(current["skill"],0)
        return f"You can consider skipping {current['skill']} only if your verified proficiency is around 80%+. Your current evidence is {score:.0f}%, so I recommend a short assessment before skipping it."
    if "time" in q:
        return f"Your plan currently assumes about {profile.get('hours_per_day',2)} hours/day over {profile.get('months',6)} months. Prioritize the highest-gap prerequisite chain first."
    return "I can explain your next-best action, skill gaps, prerequisites, assessment results, or how to compress the roadmap around your available study time."
