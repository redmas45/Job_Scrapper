import requests
from bs4 import BeautifulSoup
import time
import random

BASE_URL = "https://in.indeed.com/jobs"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9",
}


def scrape_indeed(query="AI Engineer", location="India", pages=2):
    jobs = []

    for page in range(pages):
        params = {
            "q": query,
            "l": location,
            "start": page * 10
        }

        response = requests.get(BASE_URL, headers=HEADERS, params=params)
        soup = BeautifulSoup(response.text, "html.parser")

        for job in soup.find_all("div", class_="job_seen_beacon"):
            title = job.find("h2")
            company = job.find("span", class_="companyName")
            location = job.find("div", class_="companyLocation")
            link = job.find("a")

            if not title:
                continue

            jobs.append({
                "title": title.text.strip(),
                "company": company.text.strip() if company else "",
                "location": location.text.strip() if location else "",
                "link": "https://in.indeed.com" + link["href"] if link else ""
            })

        time.sleep(random.uniform(1, 2))

    return jobs