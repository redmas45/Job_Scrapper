import json
import os
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

INDEX_PATH = os.path.join(BASE_DIR, "embeddings", "faiss.index")
META_PATH = os.path.join(BASE_DIR, "embeddings", "metadata.json")

model = SentenceTransformer("all-MiniLM-L6-v2")


def load_index():
    index = faiss.read_index(INDEX_PATH)

    with open(META_PATH, "r") as f:
        metadata = json.load(f)

    return index, metadata


def search(query, top_k=5):
    index, metadata = load_index()

    query_vector = model.encode([query]).astype("float32")

    distances, indices = index.search(query_vector, top_k)

    results = []

    for i in indices[0]:
        results.append(metadata[i])

    return results


if __name__ == "__main__":
    query = input("Enter your query: ")

    results = search(query)

    print("\nTop Matches:\n")

    for job in results:
        print(f"{job['title']} | {job['company']} | {job['location']}")