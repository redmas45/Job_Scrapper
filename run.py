import os
import json

from scraper.indeed_scraper import scrape_indeed
from scraper.remoteok import scrape_remoteok

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


# 🔥 FILTER FUNCTION
def filter_jobs(jobs):
    keywords = [
        "computer vision",
        "machine learning",
        "ai engineer",
        "ml engineer",
        "deep learning",
        "genai"
    ]

    filtered = []

    for job in jobs:
        title = job["title"].lower()

        if any(keyword in title for keyword in keywords):
            filtered.append(job)

    return filtered


def run():
    jobs = []

    # 🎯 TARGETED SEARCH
    jobs += scrape_indeed("Computer Vision Engineer", pages=2)
    jobs += scrape_indeed("Machine Learning Engineer", pages=2)
    jobs += scrape_indeed("AI Engineer", pages=2)

    jobs += scrape_remoteok()

    print(f"Total scraped: {len(jobs)}")

    # 🔥 FILTER
    jobs = filter_jobs(jobs)

    print(f"After filtering: {len(jobs)}")

    # ensure data folder exists
    os.makedirs(os.path.join(BASE_DIR, "data"), exist_ok=True)

    with open(os.path.join(BASE_DIR, "data", "jobs.json"), "w") as f:
        json.dump(jobs, f, indent=4)

    print("Saved clean jobs to data/jobs.json")


if __name__ == "__main__":
    run()