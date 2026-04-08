from data.save_jobs import save_jobs
from embeddings.embed_jobs import build_index
from embeddings.search_jobs import search
from rag.generate import generate_answer


# 🧠 Detect if query is CV-related
def is_cv_question(query):
    keywords = [
        "cv", "resume", "my experience", "my skills",
        "i worked", "what did i", "sensor", "skills",
        "experience", "technologies"
    ]
    query = query.lower()
    return any(k in query for k in keywords)


def run_pipeline():
    print("""
Choose mode:
1 → Full pipeline (scrape + embed + search)
2 → Fast mode (use existing DB + FAISS)
3 → Only scrape
4 → Only embed
""")

    choice = input("Enter choice: ").strip()

    # 🔥 MODE 1: FULL
    if choice == "1":
        print("\n🔄 Step 1: Fetching jobs...")
        save_jobs()

        print("\n🔄 Step 2: Updating embeddings...")
        build_index()

    # ⚡ MODE 2: FAST
    elif choice == "2":
        print("\n⚡ Fast mode (using existing data)")

    # 🧩 MODE 3: ONLY SCRAPE
    elif choice == "3":
        print("\n🔄 Scraping only...")
        save_jobs()
        return

    # 🧩 MODE 4: ONLY EMBED
    elif choice == "4":
        print("\n🔄 Embedding only...")
        build_index()
        return

    else:
        print("❌ Invalid choice")
        return

    # 🧠 CV SELECTION
    print("""
Select CV:
1 → CV 1 - GEN_AI
2 → CV 2 - Computer Vision
""")

    cv_choice = input("Enter CV choice: ").strip()

    # 💬 CHAT LOOP
    print("\n💬 Enter queries (type 'exit' to quit)\n")

    while True:
        query = input("🔍 Query: ").strip()

        if query.lower() in ["exit", "quit"]:
            print("\n👋 Exiting...")
            break

        if not query:
            continue

        # 🧠 ROUTING LOGIC
        if is_cv_question(query):
            print("\n🧠 Answering from CV only...")
            jobs = []  # 🚨 NO JOB CONTEXT
        else:
            print("\n🔄 Searching jobs...")
            jobs = search(query)

        print("\n🔄 Generating answer...")
        answer = generate_answer(query, jobs, cv_choice)

        print("\n💡 RESULT:\n")
        print(answer)
        print("\n" + "-"*50 + "\n")


if __name__ == "__main__":
    run_pipeline()