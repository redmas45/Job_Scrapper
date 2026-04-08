import requests
from bs4 import BeautifulSoup

BASE_URL = "https://remoteok.com/remote-ai-jobs"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9",
}


def scrape_remoteok():
    response = requests.get(BASE_URL, headers=HEADERS)
    soup = BeautifulSoup(response.text, "html.parser")

    jobs = []

    for job in soup.select("tr.job"):
        # skip invalid rows
        if "closed" in job.get("class", []):
            continue

        title_tag = job.select_one("h2")
        company_tag = job.select_one("h3")
        link = job.get("data-href")

        if not title_tag or not company_tag:
            continue

        jobs.append({
            "title": title_tag.text.strip(),
            "company": company_tag.text.strip(),
            "location": "Remote",
            "link": "https://remoteok.com" + link if link else ""
        })

    return jobs