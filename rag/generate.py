import requests
from config import GROK_API_KEY
from rag.read_cv import read_cv


def generate_answer(query, jobs, cv_choice="1"):
    try:
        if not GROK_API_KEY:
            return "❌ Missing Groq API key in server environment."

        # ================================
        # 🔥 READ CV
        # ================================
        cv_text = read_cv(cv_choice)

        # ================================
        # 🔥 BUILD CONTEXT
        # ================================
        context = ""

        for job in jobs:
            link = (job.get("link") or "").strip()

            if not link or link.lower() == "not available":
                link_text = "Not available"
            else:
                link_text = link

            context += f"""
Title: {job.get('title', '')}
Company: {job.get('company', '')}
Location: {job.get('location', '')}
Apply: {link_text}

Description:
{job.get('text', '')}

---------------------
"""

        # ================================
        # 🔥 PROMPT
        # ================================
        prompt = f"""
You are a professional AI Job Assistant.

Your job is to return CLEAN, WELL-FORMATTED answers.

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

====================
STRICT RESPONSE RULES
====================

1. DO NOT write paragraphs
2. ALWAYS use proper spacing and line breaks
3. DO NOT use '*' or messy symbols
4. Use clean bullet formatting
5. Each job MUST be clearly separated

--------------------

### FORMAT (MANDATORY)

🔹 Recommended Jobs:

1. Job Title — Company  
   📍 Location:  
   🔗 Apply:  
   ✅ Why it matches:
   - Point 1
   - Point 2

2. Job Title — Company  
   📍 Location:  
   🔗 Apply:  
   ✅ Why it matches:
   - Point 1
   - Point 2

--------------------

If no jobs found:

❌ No relevant jobs found.

--------------------

Now generate the response.
"""

        # ================================
        # 🔥 MODEL FALLBACK SYSTEM
        # ================================
        models = [
            "llama-3.3-70b-versatile",
            "llama-3.1-8b-instant",
            "openai/gpt-oss-20b",
        ]

        model_errors = []

        for model in models:
            try:
                print(f"🔄 Trying model: {model}")

                response = requests.post(
                    "https://api.groq.com/openai/v1/chat/completions",
                    headers={
                        "Authorization": f"Bearer {GROK_API_KEY}",
                        "Content-Type": "application/json"
                    },
                    json={
                        "model": model,
                        "messages": [
                            {
                                "role": "system",
                                "content": "Strictly follow formatting. Never skip Apply links if present."
                            },
                            {
                                "role": "user",
                                "content": prompt
                            }
                        ],
                        "temperature": 0.2,
                        "max_tokens": 500
                    },
                    timeout=30
                )

                data = response.json()

                if response.ok and "choices" in data:
                    print(f"✅ Using model: {model}")
                    return data["choices"][0]["message"]["content"]

                error_message = ""
                if isinstance(data, dict):
                    error = data.get("error", {})
                    if isinstance(error, dict):
                        error_message = error.get("message", "")
                    elif error:
                        error_message = str(error)

                if not error_message:
                    error_message = str(data)[:300]

                model_error = f"{model}: HTTP {response.status_code} - {error_message}"
                print(f"⚠️ Model failed: {model_error}")
                model_errors.append(model_error)

            except Exception as e:
                print(f"❌ Error with {model}: {e}")
                model_errors.append(f"{model}: {str(e)}")
                continue

        if model_errors:
            return "❌ LLM provider error:\n" + "\n".join(model_errors[:3])

        return "❌ All models failed. Please try again."

    except Exception as e:
        return f"❌ Error: {str(e)}"
