from sentence_transformers import SentenceTransformer
from config import EMBED_MODEL
from rag.read_cv import read_cv

model = SentenceTransformer(EMBED_MODEL)

# ================================
# ⚠️ FAISS LOGIC (DISABLED)
# ================================
# import faiss
# import json
# INDEX_PATH = "embeddings/faiss.index"
# META_PATH = "embeddings/metadata.json"
#
# def _search_faiss(query, top_k=5):
#     index = faiss.read_index(INDEX_PATH)
#     with open(META_PATH, "r") as f:
#         metadata = json.load(f)
#
#     query_vector = model.encode([query], normalize_embeddings=True)
#     scores, indices = index.search(query_vector, top_k)
#
#     return [metadata[i] for i in indices[0]]

# ================================
# ✅ PINECONE SEARCH
# ================================

def search(query, top_k=20, cv_choice="1"):
    return _search_pinecone(query, top_k, cv_choice)


def _search_pinecone(query, top_k=20, cv_choice="1"):
    try:
        from vector_db.pinecone_client import init_pinecone

        index = init_pinecone()
        if not index:
            return []

        cv_text = read_cv(cv_choice)

        enhanced_query = f"""
User Query: {query}

User CV:
{cv_text[:1000]}

Find best matching jobs based on skills and experience.
"""

        emb = model.encode(enhanced_query).tolist()

        res = index.query(
            vector=emb,
            top_k=top_k,
            include_metadata=True
        )

        # Deduplicate
        seen = set()
        results = []

        for match in res.get("matches", []):
            meta = match["metadata"]
            key = (meta.get("title"), meta.get("company"))

            if key not in seen:
                seen.add(key)
                results.append(meta)

        return results[:5]

    except Exception as e:
        print(f"❌ Pinecone search error: {e}")
        return []