import json
import os
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DATA_PATH = os.path.join(BASE_DIR, "data", "jobs.json")
INDEX_PATH = os.path.join(BASE_DIR, "embeddings", "faiss.index")
META_PATH = os.path.join(BASE_DIR, "embeddings", "metadata.json")

# Load FREE HuggingFace model
model = SentenceTransformer("all-MiniLM-L6-v2")


def load_jobs():
    with open(DATA_PATH, "r") as f:
        return json.load(f)


def prepare_text(job):
    return f"""
    Title: {job.get('title', '')}
    Company: {job.get('company', '')}
    Location: {job.get('location', '')}
    Description: {job.get('description', '')}
    """


def build_index():
    jobs = load_jobs()

    texts = [prepare_text(job) for job in jobs]

    print("Creating embeddings...")

    embeddings = model.encode(texts, show_progress_bar=True)

    embeddings = np.array(embeddings).astype("float32")

    dim = embeddings.shape[1]

    index = faiss.IndexFlatL2(dim)
    index.add(embeddings)

    os.makedirs(os.path.dirname(INDEX_PATH), exist_ok=True)

    faiss.write_index(index, INDEX_PATH)

    with open(META_PATH, "w") as f:
        json.dump(jobs, f, indent=4)

    print(f"Indexed {len(jobs)} jobs!")


if __name__ == "__main__":
    build_index()