import json
import urllib.request
from models import Job


def scrape() -> list[Job]:
    """Scrapes remote jobs from WorkingNomads via public endpoint or fallback."""
    jobs = []
    url = "https://www.workingnomads.com/jobsapi/job/_search?sort=created:desc&size=50"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "application/json",
    }

    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read().decode("utf-8", errors="ignore"))
            hits = data.get("hits", {}).get("hits", [])

            for hit in hits:
                source = hit.get("_source", {})
                title = source.get("title", "")
                company = source.get("company_name", "")
                job_url = source.get("url", "")
                location = source.get("location", "Remote")
                description = source.get("description", "")

                if title and job_url:
                    jobs.append(
                        Job(
                            title=title.strip(),
                            company=company.strip(),
                            url=job_url.strip(),
                            source="WorkingNomads",
                            location=str(location).strip(),
                            description=description.strip(),
                        )
                    )
    except Exception as e:
        print(f"Aviso al scrapear WorkingNomads: {e}")

    return jobs
