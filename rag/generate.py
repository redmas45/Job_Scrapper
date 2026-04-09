import requests
from config import GROK_API_KEY


def generate_answer(query, jobs, cv_text):
    try:
        # ================================
        # 🔥 BUILD CONTEXT (UNCHANGED)
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
        # 🔥 PROMPT (UNCHANGED)
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
            "llama3-70b-8192",
            "llama-3.1-8b-instant",
            "groq/compound",
            "groq/compound-mini"
        ]

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
                    }
                )

                data = response.json()

                # ✅ Success condition
                if "choices" in data:
                    print(f"✅ Using model: {model}")
                    return data["choices"][0]["message"]["content"]

                else:
                    print(f"⚠️ Model failed: {model} → {data}")

            except Exception as e:
                print(f"❌ Error with {model}: {e}")
                continue

        return "❌ All models failed"

    except Exception as e:
        return f"Error: {str(e)}"