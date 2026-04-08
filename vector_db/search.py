import json
import os
from sentence_transformers import SentenceTransformer

# Try to use FAISS first (local and fast)
try:
    import faiss
    INDEX_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "embeddings", "faiss.index")
    META_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "embeddings", "metadata.json")
    USE_FAISS = os.path.exists(INDEX_PATH) and os.path.exists(META_PATH)
except:
    USE_FAISS = False

# Lazy Pinecone initialization
USE_PINECONE = not USE_FAISS

from config import EMBED_MODEL
model = SentenceTransformer(EMBED_MODEL)


def search(query, top_k=5):
    if USE_FAISS:
        return _search_faiss(query, top_k)
    elif USE_PINECONE:
        return _search_pinecone(query, top_k)
    else:
        return []


def _search_faiss(query, top_k=5):
    """Search using local FAISS index"""
    try:
        index = faiss.read_index(INDEX_PATH)
        with open(META_PATH, "r") as f:
            metadata = json.load(f)
        
        query_vector = model.encode([query], normalize_embeddings=True)
        scores, indices = index.search(query_vector, top_k)
        
        return [metadata[str(i)] if str(i) in metadata else metadata[i] for i in indices[0] if i < len(metadata)]
    except Exception as e:
        print(f"⚠️ FAISS search error: {e}")
        return []


def _search_pinecone(query, top_k=5):
    """Search using Pinecone (lazy init)"""
    try:
        from vector_db.pinecone_client import init_pinecone
        index = init_pinecone()
        
        if not index:
            return []
        
        emb = model.encode(query).tolist()
        res = index.query(vector=emb, top_k=top_k, include_metadata=True, timeout=10)
        return [m["metadata"] for m in res.get("matches", [])]
    except Exception as e:
        print(f"⚠️ Pinecone search error: {e}")
        return []