from jobspy import scrape_jobs
import pandas as pd
import time

from data.db import create_table, insert_jobs, delete_old_jobs

ROLES = [
    "Machine Learning Engineer",
    "AI Engineer",
    "Computer Vision Engineer",
    "Generative AI Engineer",
]

SITES = ["indeed", "linkedin", "google", "zip_recruiter"]

INDIA_LOCATIONS = ["India"]

REMOTE_LOCATIONS = [
    "United States", "United Kingdom", "Germany",
    "Netherlands", "Canada", "Australia", "Singapore"
]


def fetch(role, location, remote=False, results=200):
    try:
        df = scrape_jobs(
            site_name=SITES,
            search_term=role,
            location=location,
            results_wanted=results,
            hours_old=24,
            country_indeed="India",
            remote=remote,
            verbose=0,
        )

        print(f"  ✓ {len(df):>4} jobs [{location}] {role}")
        return df

    except Exception as e:
        print(f"  ✗ Error [{location}] {role}: {e}")
        return pd.DataFrame()


def save_jobs():
    print("\n🚀 Starting job collection...\n")

    create_table()
    delete_old_jobs(hours=72)

    frames = []

    print("── India jobs ──")
    for role in ROLES:
        frames.append(fetch(role, "India", remote=False))
        time.sleep(1)

    print("\n── Remote jobs ──")
    for role in ROLES:
        for loc in REMOTE_LOCATIONS:
            frames.append(fetch(role, loc, remote=True, results=150))
            time.sleep(1)

    frames = [f for f in frames if not f.empty]

    if not frames:
        print("❌ No jobs fetched")
        return

    df = pd.concat(frames, ignore_index=True)

    print(f"\nRaw jobs: {len(df)}")

    df = df.fillna("")
    df.drop_duplicates(subset=["title", "company", "location"], inplace=True)

    df = df[df["title"] != ""]
    df = df[df["company"] != ""]

    jobs = df.to_dict(orient="records")

    print(f"Clean jobs: {len(jobs)}")

    insert_jobs(jobs)

    print("✅ Jobs stored in SQLite\n")


if __name__ == "__main__":
    save_jobs()