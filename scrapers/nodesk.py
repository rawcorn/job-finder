import html
import re
import urllib.request
from models import Job


def scrape() -> list[Job]:
    """Scrapes remote jobs from NoDesk via XML feed."""
    jobs = []
    url = "https://nodesk.co/remote-jobs/index.xml"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }

    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=15) as resp:
            xml_text = resp.read().decode("utf-8", errors="ignore")

            for item_match in re.finditer(r"<item>(.*?)</item>", xml_text, re.DOTALL):
                item_str = item_match.group(1)

                title_m = re.search(r"<title>(.*?)</title>", item_str, re.DOTALL)
                link_m = re.search(r"<link>(.*?)</link>", item_str, re.DOTALL)
                desc_m = re.search(r"<description>(.*?)</description>", item_str, re.DOTALL)

                raw_title = html.unescape(title_m.group(1).strip()) if title_m else ""
                url_str = link_m.group(1).strip() if link_m else ""
                raw_desc = html.unescape(desc_m.group(1).strip()) if desc_m else ""

                desc_clean = re.sub(r"<[^>]+>", " ", raw_desc)

                # Extraer compañía si viene con "at Company"
                title = raw_title
                company = ""
                if " at " in raw_title:
                    parts = raw_title.split(" at ", 1)
                    title = parts[0].strip()
                    company = parts[1].strip()

                if url_str:
                    jobs.append(
                        Job(
                            title=title,
                            company=company,
                            url=url_str,
                            source="NoDesk",
                            location="Remote",
                            description=desc_clean.strip(),
                        )
                    )
    except Exception as e:
        print(f"Aviso al scrapear NoDesk: {e}")

    return jobs
