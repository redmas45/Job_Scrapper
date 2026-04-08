from fastapi import FastAPI, Header, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from config import API_KEY
from vector_db.search import search
from rag.generate import generate_answer

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
    print("✅ FastAPI app started successfully!")


@app.get("/health")
def health_check():
    return {"status": "ok", "message": "Backend is running"}


@app.post("/ask")
def ask(req: QueryRequest, x_api_key: str = Header(None)):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API key")

    jobs = [] if is_cv_question(req.query) else search(req.query)

    answer = generate_answer(req.query, jobs, req.cv)

    return {"answer": answer}