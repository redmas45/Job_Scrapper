from sentence_transformers import SentenceTransformer
from config import EMBED_MODEL
from rag.read_cv import read_cv
import re

model = SentenceTransformer(EMBED_MODEL)

# ================================
# 🔥 CONSTANTS
# ================================
ROLES = [
    "Machine Learning Engineer",
    "AI Engineer",
    "Computer Vision Engineer",
    "Generative AI Engineer",
]

LOCATIONS = [
    "India",
    "United States", "USA",
    "United Kingdom", "UK",
    "Germany", "Netherlands",
    "Canada", "Australia", "Singapore"
]

# ================================
# 🔥 QUERY PARSER
# ================================
def parse_query(query):
    query_lower = query.lower()

    # Extract number (top_k)
    k_match = re.search(r'\b(\d+)\b', query_lower)
    top_k = int(k_match.group(1)) if k_match else 5

    # Extract role
    role = None
    for r in ROLES:
        if r.lower() in query_lower:
            role = r
            break

    # Extract location
    location = None
    for loc in LOCATIONS:
        if loc.lower() in query_lower:
            location = loc
            break

    return {
        "top_k": top_k,
        "role": role,
        "location": location
    }

# ================================
# 🔥 FILTER BUILDER
# ================================
def build_filter(parsed):
    filter_dict = {}

    if parsed["location"]:
        filter_dict["location"] = {"$in": [parsed["location"]]}

    if parsed["role"]:
        filter_dict["title"] = {"$in": [parsed["role"]]}

    return filter_dict if filter_dict else None

# ================================
# 🔥 MAIN SEARCH
# ================================
def search(query, cv_choice="1"):
    try:
        from vector_db.pinecone_client import init_pinecone

        index = init_pinecone()
        if not index:
            return []

        # 🔥 Parse query
        parsed = parse_query(query)
        filter_dict = build_filter(parsed)

        # 🔥 CV-aware query
        cv_text = read_cv(cv_choice)

        enhanced_query = f"""
User Query: {query}

User CV:
{cv_text[:1000]}

Find best matching jobs based on skills and experience.
"""

        emb = model.encode(enhanced_query).tolist()

        # 🔥 Query Pinecone
        res = index.query(
            vector=emb,
            top_k=50,
            include_metadata=True,
            filter=filter_dict
        )

        # 🔥 Deduplicate
        seen = set()
        results = []

        for match in res.get("matches", []):
            meta = match["metadata"]
            key = (meta.get("title"), meta.get("company"))

            if key not in seen:
                seen.add(key)
                results.append(meta)

        return results[:parsed["top_k"]]

    except Exception as e:
        print(f"❌ Search error: {e}")
        return []