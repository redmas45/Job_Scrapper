from sentence_transformers import SentenceTransformer
from config import EMBED_MODEL
from data.db import fetch_all_jobs
from vector_db.pinecone_client import init_pinecone
import uuid

model = SentenceTransformer(EMBED_MODEL)


def chunk_text(text, size=200):
    words = text.split()
    return [" ".join(words[i:i+size]) for i in range(0, len(words), size)]


def embed_and_upload():
    jobs = fetch_all_jobs()

    index = init_pinecone()
    if not index:
        print("❌ Pinecone not initialized")
        return

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

    # Batch upload
    batch_size = 100
    for i in range(0, len(vectors), batch_size):
        index.upsert(vectors=vectors[i:i+batch_size])

    print(f"✅ Uploaded {len(vectors)} chunks to Pinecone")