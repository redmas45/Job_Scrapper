import requests
from config import GROK_API_KEY
from rag.read_cv import read_cv


def generate_answer(query, jobs, cv_choice="1"):
    cv_text = read_cv(cv_choice)

    if jobs:
        context = "\n\n".join([
            f"{job['title']} at {job['company']} ({job['location']})\n{job.get('text','')}"
            for job in jobs
        ])
    else:
        context = "No job context"

    # ✅ SAME PROMPT (UNCHANGED)
    prompt = f"""
You are an AI assistant.

You have access to the user's CV.

====================
USER CV:
{cv_text}
====================

USER QUERY:
{query}

====================
JOB LISTINGS:
{context}
====================

INSTRUCTIONS:

1. If the question is about the CV:
   - Answer ONLY using CV
   - DO NOT mention jobs
   - DO NOT guess
   - If not found → say "Not found in CV"

2. If the question is about jobs:
   - Use BOTH CV and job listings
   - Recommend only relevant jobs
   - Explain WHY they match CV
"""

    # 🔥 GROK API CALL (OpenAI-compatible format)
    response = requests.post(
        "https://api.x.ai/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {GROK_API_KEY}",
            "Content-Type": "application/json"
        },
        json={
            "model": "grok-beta",
            "messages": [
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.3,
            "max_tokens": 500
        }
    )

    data = response.json()

    return data.get("choices", [{}])[0].get("message", {}).get("content", "No response")