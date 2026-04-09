import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


def as_bool(value: str, default: bool = False) -> bool:
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "on"}

# 🔐 Pinecone Config
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY", "").strip()
PINECONE_INDEX = os.getenv("PINECONE_INDEX", "jobs-index")


# 🤖 Groq Config
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "").strip()
GROK_API_KEY = GROQ_API_KEY or os.getenv("GROK_API_KEY", "").strip()

# 🧠 Embedding Model (using smaller distilroberta for faster loading)
EMBED_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

# 🔑 API Security Key
API_KEY = os.getenv("API_KEY", "change-me-in-production").strip()
REQUIRE_API_KEY = as_bool(os.getenv("REQUIRE_API_KEY"), default=False)
