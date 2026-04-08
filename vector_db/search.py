from sentence_transformers import SentenceTransformer
from config import EMBED_MODEL
from vector_db.pinecone_client import index

model = SentenceTransformer(EMBED_MODEL)


def search(query, top_k=5):
    emb = model.encode(query).tolist()

    res = index.query(vector=emb, top_k=top_k, include_metadata=True)

    return [m["metadata"] for m in res["matches"]]