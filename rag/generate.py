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

        print(f"🔥 Calling Grok API with query: {query[:50]}...")
        print(f"🔑 API Key present: {bool(GROK_API_KEY)}")

        # 🔥 GROK API CALL (OpenAI-compatible format)
        response = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {GROK_API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": "llama3-8b-8192",
                "messages": [
                    {"role": "user", "content": prompt}
                ],
                "temperature": 0.4,
                "max_tokens": 500
            },
            timeout=30
        )

        print(f"📡 Grok API Status: {response.status_code}")

        if response.status_code != 200:
            print(f"❌ Grok API Error: {response.status_code}")
            print(f"Response: {response.text}")
            return f"Error from LLM: {response.status_code} - {response.text[:200]}"

        data = response.json()
        answer = data.get("choices", [{}])[0].get("message", {}).get("content", "")
        
        if not answer:
            print(f"⚠️ No content in response: {data}")
            return "Could not generate answer. Please try again."

        return answer

    except requests.exceptions.Timeout:
        return "❌ Error: LLM API request timed out (>30s). Try again."
    except requests.exceptions.ConnectionError:
        return "❌ Error: Cannot connect to LLM API. Check internet connection."
    except Exception as e:
        print(f"💥 Generate error: {type(e).__name__}: {e}")
        return f"❌ Error: {type(e).__name__}: {str(e)[:100]}"