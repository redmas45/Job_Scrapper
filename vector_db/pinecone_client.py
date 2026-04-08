from pinecone import Pinecone, ServerlessSpec
from config import PINECONE_API_KEY, PINECONE_INDEX

# 🔐 Init Pinecone
pc = Pinecone(api_key=PINECONE_API_KEY)

# 📦 Get existing indexes
existing_indexes = [i.name for i in pc.list_indexes()]

# 🆕 Create index if not exists
if PINECONE_INDEX not in existing_indexes:
    pc.create_index(
        name=PINECONE_INDEX,
        dimension=384,
        metric="cosine",
        spec=ServerlessSpec(cloud="aws", region="us-east-1")
    )

# 🔥 IMPORTANT: expose index variable
index = pc.Index(PINECONE_INDEX)