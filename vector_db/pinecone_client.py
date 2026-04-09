from pinecone import Pinecone, ServerlessSpec
from config import PINECONE_API_KEY, PINECONE_INDEX

index = None


def init_pinecone():
    global index

    if index:
        return index

    try:
        pc = Pinecone(api_key=PINECONE_API_KEY)

        existing = [i.name for i in pc.list_indexes()]

        if PINECONE_INDEX not in existing:
            pc.create_index(
                name=PINECONE_INDEX,
                dimension=384,
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