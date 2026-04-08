import requests

OLLAMA_URL = "http://localhost:11434/api/generate"

def generate_answer(query, jobs):
    context = "\n\n".join([
        f"{job['title']} at {job['company']} in {job['location']}"
        for job in jobs
    ])

    prompt = f"""
You are an AI job assistant.

User query: {query}

Here are relevant jobs:
{context}

Task:
- Recommend best jobs
- Explain why they match
- Keep answer short and clear
"""

    response = requests.post(OLLAMA_URL, json={
        "model": "gemma4",
        "prompt": prompt,
        "stream": False
    })

    return response.json()["response"]