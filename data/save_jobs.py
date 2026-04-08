import json
from main import collect_jobs


def save_jobs():
    jobs = collect_jobs()

    with open("data/jobs.json", "w") as f:
        json.dump(jobs, f, indent=4)

    print(f"Saved {len(jobs)} jobs to data/jobs.json")


if __name__ == "__main__":
    save_jobs()