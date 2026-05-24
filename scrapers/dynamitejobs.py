import html
import re
import urllib.request
from models import Job


def scrape() -> list[Job]:
    """Scrapes remote jobs from DynamiteJobs."""
    jobs = []
    url = "https://dynamitejobs.com/remote-jobs"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }

    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=15) as resp:
            content = resp.read().decode("utf-8", errors="ignore")

            pattern = re.compile(
                r'<a[^>]+href=["\'](/company/[^/]+/job/[^"\']+)["\'][^>]*>(.*?)</a>',
                re.DOTALL | re.IGNORECASE,
            )

            seen = set()
            for m in pattern.finditer(content):
                relative_url = m.group(1).strip()
                if relative_url in seen:
                    continue
                seen.add(relative_url)

                full_url = f"https://dynamitejobs.com{relative_url}"
                text = re.sub(r"<[^>]+>", " ", m.group(2))
                clean_text = html.unescape(text).strip()

                if clean_text:
                    jobs.append(
                        Job(
                            title=clean_text,
                            company="",
                            url=full_url,
                            source="DynamiteJobs",
                            location="Remote",
                            description="",
                        )
                    )
    except Exception as e:
        print(f"Aviso al scrapear DynamiteJobs: {e}")

    return jobs
