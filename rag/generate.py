import requests
from rag.read_cv import read_cv

OLLAMA_URL = "http://localhost:11434/api/generate"


def generate_answer(query, jobs, cv_choice="1"):
    cv_text = read_cv(cv_choice)

    context = "\n\n".join([
        f"{job['title']} at {job['company']} ({job['location']})"
        for job in jobs
    ])

    prompt = f"""
You are an AI job assistant.

User CV:
{cv_text}

User Query:
{query}

Jobs:
{context}

Task:
1. Recommend top jobs based on CV
2. Explain why they match skills
3. Keep answer concise
"""

    response = requests.post(OLLAMA_URL, json={
        "model": "gemma4",
        "prompt": prompt,
        "stream": False
    })

    return response.json()["response"]