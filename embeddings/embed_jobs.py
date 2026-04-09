from sentence_transformers import SentenceTransformer
from config import EMBED_MODEL
from data.db import fetch_all_jobs
from vector_db.pinecone_client import init_pinecone
import uuid
from tqdm import tqdm

model = SentenceTransformer(EMBED_MODEL)


def chunk_text(text, size=200):
    words = text.split()
    return [" ".join(words[i:i+size]) for i in range(0, len(words), size)]


def embed_and_upload():
    print("📦 Loading jobs from DB...")
    jobs = fetch_all_jobs()

    if not jobs:
        print("❌ No jobs found in DB")
        return

    print(f"✅ Found {len(jobs)} jobs")

    index = init_pinecone()
    if not index:
        print("❌ Pinecone not initialized")
        return

    vectors = []

    # 🔥 Process jobs
    for job in tqdm(jobs, desc="🔄 Processing Jobs"):
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

    print(f"\n🧠 Total chunks: {len(vectors)}")

    # 🔥 Upload with safety
    batch_size = 100

    for i in tqdm(range(0, len(vectors), batch_size), desc="⬆️ Uploading"):
        batch = vectors[i:i+batch_size]

        try:
            index.upsert(vectors=batch)
        except Exception as e:
            print(f"⚠️ Batch failed at {i}: {e}")

    print("✅ Pinecone sync complete")