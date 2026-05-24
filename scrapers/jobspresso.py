import html
import re
import urllib.request
from models import Job


def scrape() -> list[Job]:
    """Scrapes remote jobs from Jobspresso."""
    jobs = []
    url = "https://jobspresso.co/remote-work/"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }

    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=15) as resp:
            content = resp.read().decode("utf-8", errors="ignore")

            # Buscar elementos con enlaces a /job/
            pattern = re.compile(
                r'<a[^>]+href=["\'](https://jobspresso\.co/job/[^"\']+)["\'][^>]*>(.*?)</a>',
                re.DOTALL | re.IGNORECASE,
            )

            seen_urls = set()
            for match in pattern.finditer(content):
                job_url = match.group(1).strip()
                link_inner = match.group(2)

                if job_url in seen_urls:
                    continue
                seen_urls.add(job_url)

                text = re.sub(r"<[^>]+>", " ", link_inner)
                clean_text = html.unescape(text).strip()

                if clean_text:
                    jobs.append(
                        Job(
                            title=clean_text,
                            company="",
                            url=job_url,
                            source="Jobspresso",
                            location="Remote",
                            description="",
                        )
                    )
    except Exception as e:
        print(f"Aviso al scrapear Jobspresso: {e}")

    return jobs
