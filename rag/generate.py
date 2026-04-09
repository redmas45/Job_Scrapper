from groq import Groq
from config import GROK_API_KEY


client = Groq(api_key=GROK_API_KEY)


def generate_response(query, jobs, cv_text):
    # ================================
    # 🔥 BUILD CONTEXT (FIXED LINKS)
    # ================================
    context = ""

    for job in jobs:
        link = job.get("link", "").strip()

        # 🔥 Ensure clean link handling
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
    # 🔥 YOUR ORIGINAL PROMPT (UNCHANGED)
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
    # 🔥 CALL LLM
    # ================================
    response = client.chat.completions.create(
        model="llama3-70b-8192",
        messages=[
            {"role": "user", "content": prompt}
        ],
        temperature=0.2
    )

    return response.choices[0].message.content