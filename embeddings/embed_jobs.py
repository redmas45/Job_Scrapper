import os
import faiss
import json
from sentence_transformers import SentenceTransformer
from data.db import fetch_unembedded_jobs, mark_jobs_embedded

INDEX_PATH = "embeddings/faiss.index"
META_PATH = "embeddings/metadata.json"

MODEL_NAME = "all-MiniLM-L6-v2"
model = SentenceTransformer(MODEL_NAME)


def prepare_text(job):
    title = (job.get("title") or "").lower()
    company = (job.get("company") or "").lower()
    location = (job.get("location") or "").lower()
    desc = (job.get("description") or "")[:1500].lower()

    return f"Title: {title} {title}\nCompany: {company}\nLocation: {location}\nDescription: {desc}"


def load_existing():
    if os.path.exists(INDEX_PATH):
        index = faiss.read_index(INDEX_PATH)
        with open(META_PATH, "r", encoding="utf-8") as f:
            metadata = json.load(f)
        return index, metadata
    return None, []


def save(index, metadata):
    os.makedirs("embeddings", exist_ok=True)
    faiss.write_index(index, INDEX_PATH)

    with open(META_PATH, "w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=4)


def build_index():
    jobs = fetch_unembedded_jobs()

    if not jobs:
        print("✅ No new jobs to embed")
        return

    texts = [prepare_text(j) for j in jobs]

    embeddings = model.encode(
        texts,
        batch_size=64,
        convert_to_numpy=True,
        normalize_embeddings=True
    ).astype("float32")

    index, metadata = load_existing()

    if index is None:
        index = faiss.IndexFlatIP(embeddings.shape[1])

    index.add(embeddings)
    metadata.extend(jobs)

    save(index, metadata)

    mark_jobs_embedded([j["id"] for j in jobs])

    print(f"🚀 Added {len(jobs)} new embeddings")


if __name__ == "__main__":
    build_index()