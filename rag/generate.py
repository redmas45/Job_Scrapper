import requests
from config import GROK_API_KEY
from rag.read_cv import read_cv


def generate_answer(query, jobs, cv_choice="1"):
    try:
        cv_text = read_cv(cv_choice)

        if jobs:
            context = "\n\n".join([
                f"{job['title']} at {job['company']} ({job['location']})\n{job.get('text','')}"
                for job in jobs
            ])
        else:
            context = "No job context"

        prompt = f"""
You are a STRICT AI Job Assistant.

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

RULES:
- ONLY bullet points
- NO paragraphs
- SHORT answers
- NO hallucination

--------------------

### CV QUESTION

🔹 Answer:
- Point 1
- Point 2

--------------------

### JOB RECOMMENDATION

🔹 Recommended Jobs:

1. Job Title — Company
   - 📍 Location:
   - 🔗 Apply: (if link available)
   - ✅ Why it matches:
     - Reason 1
     - Reason 2

--------------------

### NO MATCH

❌ No relevant jobs found based on your CV.
"""

        response = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {GROK_API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": "llama-3.3-70b-versatile",
                "messages": [
                    {
                        "role": "system",
                        "content": "Always respond in bullet points. Never write paragraphs."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                "temperature": 0.2,
                "max_tokens": 400
            }
        )

        data = response.json()
        return data["choices"][0]["message"]["content"]

    except Exception as e:
        return f"Error: {str(e)}"