import requests
from rag.read_cv import read_cv

OLLAMA_URL = "http://localhost:11434/api/generate"


def generate_answer(query, jobs, cv_choice="1"):
    cv_text = read_cv(cv_choice)

    # 🧠 Build job context (if exists)
    if jobs:
        context = "\n\n".join([
            f"{job['title']} at {job['company']} ({job['location']})"
            for job in jobs
        ])
    else:
        context = "No job context"

    # 🔥 STRONG PROMPT (anti-hallucination + routing)
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

3. Be precise and factual
4. Avoid generic answers
"""

    response = requests.post(OLLAMA_URL, json={
        "model": "gemma4",   # you can switch to gemma later
        "prompt": prompt,
        "stream": False
    })

    return response.json().get("response", "⚠️ No response from model")