import json
import faiss
from sentence_transformers import SentenceTransformer

INDEX_PATH = "embeddings/faiss.index"
META_PATH = "embeddings/metadata.json"

model = SentenceTransformer("all-MiniLM-L6-v2")


def search(query, top_k=5):
    index = faiss.read_index(INDEX_PATH)

    with open(META_PATH, "r") as f:
        metadata = json.load(f)

    query_vector = model.encode([query], normalize_embeddings=True)

    scores, indices = index.search(query_vector, top_k)

    return [metadata[i] for i in indices[0]]