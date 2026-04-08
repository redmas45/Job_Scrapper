from fastapi import FastAPI, Header, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
import sys

try:
    from config import API_KEY
    print("✅ Config loaded")
except Exception as e:
    print(f"❌ Config error: {e}")
    sys.exit(1)

try:
    from vector_db.search import search
    print("✅ Search module loaded")
except Exception as e:
    print(f"⚠️ Search module error: {e}")
    search = None

try:
    from rag.generate import generate_answer
    print("✅ Generate module loaded")
except Exception as e:
    print(f"⚠️ Generate module error: {e}")
    generate_answer = None

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_headers=["*"],
    allow_methods=["*"],
)


class QueryRequest(BaseModel):
    query: str
    cv: str = "1"


def is_cv_question(q):
    return any(k in q.lower() for k in ["cv", "resume", "skills", "experience", "sensor"])


@app.on_event("startup")
async def startup_event():
    print("=" * 50)
    print("🚀 FastAPI Startup")
    print(f"📁 Working directory: {os.getcwd()}")
    print(f"🔑 API Key configured: {bool(API_KEY)}")
    print(f"📁 /embeddings exists: {os.path.exists('embeddings')}")
    print(f"📁 /data exists: {os.path.exists('data')}")
    print("=" * 50)
    print("✅ FastAPI app started successfully!")


@app.get("/health")
def health_check():
    return {"status": "ok", "message": "Backend is running"}


@app.post("/ask")
def ask(req: QueryRequest, x_api_key: str = Header(None)):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API key")

    if not generate_answer:
        return {"answer": "❌ LLM module not loaded"}

    try:
        jobs = []
        if not is_cv_question(req.query) and search:
            jobs = search(req.query)
        
        answer = generate_answer(req.query, jobs, req.cv)
        return {"answer": answer}
    except Exception as e:
        return {"answer": f"❌ Error: {str(e)[:200]}"}