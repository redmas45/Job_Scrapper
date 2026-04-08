from data.save_jobs import save_jobs
from embeddings.embed_jobs import build_index
from embeddings.search_jobs import search
from rag.generate import generate_answer

def run_pipeline():
    print("\n🔄 Step 1: Fetching jobs...")
    save_jobs()

    print("\n🔄 Step 2: Creating embeddings...")
    build_index()

    query = input("\n🔍 Enter your job query: ")

    print("\n🔄 Step 3: Searching jobs...")
    jobs = search(query)

    print("\n🔄 Step 4: Generating answer...")
    answer = generate_answer(query, jobs)

    print("\n💡 FINAL RESULT:\n")
    print(answer)


if __name__ == "__main__":
    run_pipeline()