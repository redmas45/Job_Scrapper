import requests
from config import GROK_API_KEY


def generate_response(query, jobs, cv_text):
    try:
        # ================================
        # 🔥 BUILD CONTEXT (FIXED + STRONG)
        # ================================
        context = ""

        for job in jobs:
            link = (job.get("link") or "").strip()

            # 🔥 Force valid link handling
            if not link or link.lower() == "not available":
                link_text = "Not available"
            else:
                link_text = link

            context += f"""
Title: {job.get('title', '')}
Company: {job.get('company', '')}
Location: {job.get('location', '')}
Apply Link: {link_text}

Description:
{job.get('text', '')}

---------------------
"""

        # ================================
        # 🔥 YOUR PROMPT (UNCHANGED)
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
6. ALWAYS show Apply link if provided

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
        # 🔥 CALL GROQ API
        # ================================
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

        # 🔥 Safe response handling
        return data.get("choices", [{}])[0].get("message", {}).get("content", "No response")

    except Exception as e:
        return f"Error: {str(e)}"