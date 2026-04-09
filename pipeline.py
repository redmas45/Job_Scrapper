from data.save_jobs import scrape_jobs
from embeddings.embed_jobs import embed_and_upload
from vector_db.pinecone_client import init_pinecone


def scrape_only():
    print("\n🔍 Running Scraping Pipeline...\n")

    try:
        scrape_jobs()
        print("✅ Jobs scraped and saved to SQLite (.db)")
    except Exception as e:
        print(f"❌ Scraping failed: {e}")


def pinecone_only():
    print("\n🧠 Running Pinecone Upload Pipeline...\n")

    # Init Pinecone
    index = init_pinecone()
    if not index:
        print("❌ Pinecone init failed")
        return

    print("✅ Pinecone initialized")

    # Clear old data
    print("\n🧹 Clearing existing Pinecone data...")
    try:
        index.delete(delete_all=True)
        print("✅ Pinecone cleared")
    except Exception as e:
        print(f"⚠️ Could not clear Pinecone: {e}")

    # Embed & upload
    print("\n📦 Uploading DB → Pinecone...")
    try:
        embed_and_upload()
        print("✅ Pinecone updated successfully")
    except Exception as e:
        print(f"❌ Upload failed: {e}")


def main():
    print("\n🚀 PIPELINE MENU\n")
    print("1 → Scrape + Save to DB")
    print("2 → Upload DB to Pinecone")
    print("0 → Exit")

    choice = input("\nEnter your choice: ").strip()

    if choice == "1":
        scrape_only()

    elif choice == "2":
        pinecone_only()

    elif choice == "0":
        print("👋 Exiting...")

    else:
        print("❌ Invalid choice")


if __name__ == "__main__":
    main()