from fastapi import FastAPI, Header, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from vector_db.search import search
from rag.generate import generate_answer

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_headers=["*"],
    allow_methods=["*"],
)

API_KEY = "mysecret123"


class QueryRequest(BaseModel):
    query: str
    cv: str = "1"


def is_cv_question(q):
    return any(k in q.lower() for k in ["cv", "resume", "skills", "experience", "sensor"])


@app.post("/ask")
def ask(req: QueryRequest, x_api_key: str = Header(None)):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401)

    jobs = [] if is_cv_question(req.query) else search(req.query)

    answer = generate_answer(req.query, jobs, req.cv)

    return {"answer": answer}