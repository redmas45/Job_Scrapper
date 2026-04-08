from jobspy import scrape_jobs
import pandas as pd
import os
import json
import time

# 🎯 Target roles
ROLES = [
    "Machine Learning Engineer",
    "AI Engineer",
    "Computer Vision Engineer",
    "Generative AI Engineer",
]

# 🌐 Sites
SITES = ["indeed", "linkedin", "glassdoor", "google", "zip_recruiter"]

# 🇮🇳 India (onsite)
INDIA_LOCATIONS = ["India"]

# 🌍 Global remote locations
REMOTE_LOCATIONS = [
    "United States",
    "United Kingdom",
    "Germany",
    "Netherlands",
    "Canada",
    "Australia",
    "Singapore",
]


def fetch(role, location, remote=False, results=200):
    try:
        df = scrape_jobs(
            site_name=SITES,
            search_term=role,
            location=location,
            results_wanted=results,
            hours_old=24,
            country_indeed="India",   # stable default
            remote=remote,           # ✅ correct parameter
            verbose=0,
        )

        print(f"  ✓ {len(df):>4} jobs  [{location}]  {role}")
        return df

    except Exception as e:
        print(f"  ✗ Error [{location}] {role}: {e}")
        return pd.DataFrame()


def save_jobs():
    print("\n🚀 Starting job collection...\n")

    frames = []

    # 🇮🇳 India jobs
    print("── India (on-site/hybrid) ──")
    for role in ROLES:
        for loc in INDIA_LOCATIONS:
            frames.append(fetch(role, loc, remote=False, results=200))
            time.sleep(1)  # avoid rate limit

    # 🌍 Remote jobs (global)
    print("\n── Remote (worldwide) ──")
    for role in ROLES:
        for loc in REMOTE_LOCATIONS:
            frames.append(fetch(role, loc, remote=True, results=150))
            time.sleep(1)

    # ✅ Remove empty frames
    frames = [f for f in frames if not f.empty]

    if not frames:
        print("❌ No jobs fetched!")
        return

    # Combine
    df = pd.concat(frames, ignore_index=True)
    print(f"\nTotal raw        : {len(df)}")

    # 🧹 Deduplicate
    df.drop_duplicates(
        subset=["title", "company", "location"],
        inplace=True
    )
    print(f"After dedup      : {len(df)}")

    # ❌ Remove invalid rows
    df.dropna(subset=["title", "company"], inplace=True)
    print(f"After null-drop  : {len(df)}")

    # 🧠 Ensure description exists (important for RAG)
    if "description" not in df.columns:
        df["description"] = ""

    # 🧠 Fix date serialization
    if "date_posted" in df.columns:
        df["date_posted"] = df["date_posted"].astype(str)

    # Convert to JSON
    jobs = df.to_dict(orient="records")

    os.makedirs("data", exist_ok=True)

    with open("data/jobs.json", "w", encoding="utf-8") as f:
        json.dump(jobs, f, indent=4, ensure_ascii=False)

    print(f"\n✅ Saved {len(jobs)} jobs → data/jobs.json\n")


if __name__ == "__main__":
    save_jobs()