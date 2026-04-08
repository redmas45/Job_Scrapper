import os

# 🔐 Pinecone Config
PINECONE_API_KEY = os.getenv("pcsk_8wQAd_8PtcbuccftJdnpEzUvBj4i9HHD2KcHUeVK1THqgSHtki9YiC4MLWVm9Juc8Rhah")
PINECONE_INDEX = os.getenv("PINECONE_INDEX", "jobs-index")

# 🤖 Grok (XAI) Config
GROK_API_KEY = os.getenv("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")

# 🧠 Embedding Model
EMBED_MODEL = "all-MiniLM-L6-v2"