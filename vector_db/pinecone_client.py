from pinecone import Pinecone, ServerlessSpec
from config import PINECONE_API_KEY, PINECONE_INDEX

# Lazy initialization - don't block on startup
index = None

def init_pinecone():
    """Initialize Pinecone lazily on first use"""
    global index
    
    if index is not None:
        return index
    
    try:
        print("🔄 Initializing Pinecone...")
        pc = Pinecone(api_key=PINECONE_API_KEY, timeout=10)
        
        existing_indexes = [i.name for i in pc.list_indexes()]
        
        if PINECONE_INDEX not in existing_indexes:
            print(f"📦 Creating Pinecone index: {PINECONE_INDEX}")
            pc.create_index(
                name=PINECONE_INDEX,
                dimension=384,
                metric="cosine",
                spec=ServerlessSpec(cloud="aws", region="us-east-1")
            )
        
        index = pc.Index(PINECONE_INDEX)
        print("✅ Pinecone initialized")
        return index
    except Exception as e:
        print(f"⚠️ Pinecone init failed: {e}")
        return None