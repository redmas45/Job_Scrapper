import os
from data.save_jobs import scrape_jobs
from embeddings.embed_jobs import embed_and_upload
from vector_db.pinecone_client import init_pinecone

DB_PATH = "data/jobs.db"


def delete_old_db():
    if os.path.exists(DB_PATH):
        print("🧹 Deleting old SQLite database...")
        os.remove(DB_PATH)
        print("✅ Old database deleted\n")
    else:
        print("ℹ️ No existing database found\n")


def run_pipeline():
    print("🚀 Starting full pipeline...\n")

    # ================================
    # 0. DELETE OLD DATABASE
    # ================================
    delete_old_db()

    # ================================
    # 1. SCRAPE JOBS
    # ================================
    print("🔍 Step 1: Scraping jobs...")
    try:
        scrape_jobs()
        print("✅ Jobs scraped and saved to NEW SQLite DB\n")
    except Exception as e:
        print(f"❌ Scraping failed: {e}")
        return

    # ================================
    # 2. INIT PINECONE
    # ================================
    print("🧠 Step 2: Initializing Pinecone...")
    index = init_pinecone()

    if not index:
        print("❌ Pinecone initialization failed")
        return

    print("✅ Pinecone ready\n")

    # ================================
    # 3. CLEAR PINECONE
    # ================================
    print("🧹 Step 3: Clearing old vectors from Pinecone...")
    try:
        index.delete(delete_all=True)
        print("✅ Pinecone cleared\n")
    except Exception as e:
        print(f"⚠️ Could not clear Pinecone: {e}")

    # ================================
    # 4. EMBED + UPLOAD
    # ================================
    print("📦 Step 4: Embedding & uploading jobs...")
    try:
        embed_and_upload()
        print("✅ Pinecone updated successfully\n")
    except Exception as e:
        print(f"❌ Embedding failed: {e}")
        return

    # ================================
    # DONE
    # ================================
    print("🎉 PIPELINE COMPLETED SUCCESSFULLY!")


# ================================
# ENTRY POINT
# ================================
if __name__ == "__main__":
    run_pipeline()