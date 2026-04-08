from scraper.indeed_scraper import scrape_indeed
from scraper.remoteok import scrape_remoteok

def collect_jobs():
    jobs = []

    jobs += scrape_indeed("AI Engineer", pages=2)
    jobs += scrape_indeed("Machine Learning Engineer", pages=2)
    jobs += scrape_indeed("Computer Vision Engineer", pages=2)

    jobs += scrape_remoteok()

    return jobs


if __name__ == "__main__":
    jobs = collect_jobs()

    print(f"Total jobs collected: {len(jobs)}\n")

    for j in jobs[:10]:
        print(j)