from fastapi import FastAPI, Header, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
import sys

print("\n🔧 Initializing FastAPI app...\n")

# Try to load each module with error handling
try:
    from config import API_KEY
    print("✅ Config loaded")
except Exception as e:
    print(f"❌ FATAL: Config error: {e}")
    API_KEY = "mysecret123"

search = None
generate_answer = None

try:
    # Lazy import to avoid blocking
    import importlib
    from vector_db import search as search_module
    search = search_module.search
    print("✅ Search module loaded")
except Exception as e:
    print(f"⚠️ Search module failed: {e}")

try:
    from rag import generate as generate_module
    generate_answer = generate_module.generate_answer
    print("✅ Generate module loaded")
except Exception as e:
    print(f"⚠️ Generate module failed: {e}")

print("\n🚀 Creating FastAPI app...\n")

app = FastAPI(title="Job Scrapper API")

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
    print("\n" + "=" * 60)
    print("🚀 FastAPI Startup - COMPLETE")
    print("=" * 60)
    print(f"📁 Working directory: {os.getcwd()}")
    print(f"🔑 API Key configured: {bool(API_KEY)}")
    print(f"📁 /embeddings exists: {os.path.exists('embeddings')}")
    print(f"📁 /data exists: {os.path.exists('data')}")
    print(f"🔍 Search available: {search is not None}")
    print(f"📝 Generate available: {generate_answer is not None}")
    print("=" * 60 + "\n")


@app.get("/")
def root():
    return {
        "status": "ok",
        "message": "Job Scrapper API is running",
        "endpoints": ["/health", "/ask"]
    }


@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "message": "Backend is running",
        "search_available": search is not None,
        "generate_available": generate_answer is not None
    }


@app.post("/ask")
def ask(req: QueryRequest, x_api_key: str = Header(None)):
    try:
        if x_api_key != API_KEY:
            raise HTTPException(status_code=401, detail="Invalid API key")

        if not generate_answer:
            return {"answer": "❌ LLM module not loaded"}

        jobs = []
        if not is_cv_question(req.query) and search:
            try:
                jobs = search(req.query)
            except Exception as e:
                print(f"⚠️ Search error: {e}")
                jobs = []
        
        answer = generate_answer(req.query, jobs, req.cv)
        return {"answer": answer}
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Ask error: {e}")
        return {"answer": f"❌ Error: {str(e)[:200]}"}