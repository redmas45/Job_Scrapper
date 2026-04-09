from pinecone import Pinecone, ServerlessSpec
from config import PINECONE_API_KEY, PINECONE_INDEX

index = None


def init_pinecone():
    global index

    if index:
        return index

    try:
        if not PINECONE_API_KEY:
            raise ValueError("PINECONE_API_KEY is missing")

        pc = Pinecone(api_key=PINECONE_API_KEY)

        existing = [i.name for i in pc.list_indexes()]

        # 🔥 Create index with correct dimension (768)
        if PINECONE_INDEX not in existing:
            print("📦 Creating Pinecone index (768 dim)...")
            pc.create_index(
                name=PINECONE_INDEX,
                dimension=384,   # ✅ FIXED
                metric="cosine",
                spec=ServerlessSpec(
                    cloud="aws",
                    region="us-east-1"
                )
            )

        index = pc.Index(PINECONE_INDEX)
        print("✅ Pinecone initialized")

        return index

    except Exception as e:
        print(f"❌ Pinecone init error: {e}")
        return None