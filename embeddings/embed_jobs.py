from sentence_transformers import SentenceTransformer
from config import EMBED_MODEL
from data.db import fetch_all_jobs
from vector_db.pinecone_client import index
import uuid

model = SentenceTransformer(EMBED_MODEL)


def chunk_text(text, size=200):
    words = text.split()
    return [" ".join(words[i:i+size]) for i in range(0, len(words), size)]


def embed_and_upload():
    jobs = fetch_all_jobs()

    vectors = []

    for job in jobs:
        text = f"{job.get('title','')} {job.get('description','')}"
        chunks = chunk_text(text)

        for chunk in chunks:
            emb = model.encode(chunk).tolist()

            vectors.append({
                "id": str(uuid.uuid4()),
                "values": emb,
                "metadata": {
                    "title": job.get("title", ""),
                    "company": job.get("company", ""),
                    "location": job.get("location", ""),
                    "link": job.get("link", ""),
                    "text": chunk
                }
            })

    index.upsert(vectors=vectors)

    print(f"✅ Uploaded {len(vectors)} chunks")