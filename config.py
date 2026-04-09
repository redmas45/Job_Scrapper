import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# 🔐 Pinecone Config
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY", "").strip()
PINECONE_INDEX = os.getenv("PINECONE_INDEX", "jobs-index")

# 🤖 Grok (XAI) Config
GROK_API_KEY = os.getenv("GROK_API_KEY", "").strip()

# 🧠 Embedding Model (using smaller distilroberta for faster loading)
EMBED_MODEL = "sentence-transformers/all-distilroberta-v1"

# 🔑 API Security Key
API_KEY = os.getenv("API_KEY", "change-me-in-production").strip()