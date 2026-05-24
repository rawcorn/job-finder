import json
import urllib.request
from models import Job


def scrape() -> list[Job]:
    """Scrapes remote jobs from Remotive via public API."""
    jobs = []
    url = "https://remotive.com/api/remote-jobs?limit=100"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }

    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read().decode("utf-8", errors="ignore"))

            for item in data.get("jobs", []):
                jobs.append(
                    Job(
                        title=item.get("title", "").strip(),
                        company=item.get("company_name", "").strip(),
                        url=item.get("url", "").strip(),
                        source="Remotive",
                        location=item.get("candidate_required_location", "").strip(),
                        description=item.get("description", "").strip(),
                    )
                )
    except Exception as e:
        print(f"Aviso al scrapear Remotive: {e}")

    return jobs
