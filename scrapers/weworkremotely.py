import html
import re
import urllib.request
import xml.etree.ElementTree as ET
from models import Job


def scrape() -> list[Job]:
    """Scrapes remote jobs from WeWorkRemotely via RSS feed."""
    jobs = []
    url = "https://weworkremotely.com/remote-jobs.rss"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }

    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=15) as resp:
            content = resp.read()
            root = ET.fromstring(content)

            for item in root.findall(".//item"):
                title_elem = item.find("title")
                link_elem = item.find("link")
                desc_elem = item.find("description")
                region_elem = item.find("region")

                raw_title = title_elem.text if title_elem is not None and title_elem.text else ""
                url_str = link_elem.text if link_elem is not None and link_elem.text else ""
                desc = desc_elem.text if desc_elem is not None and desc_elem.text else ""
                location = region_elem.text if region_elem is not None and region_elem.text else ""

                # Limpiar tags HTML en la descripción si vienen presentes
                desc_clean = re.sub(r"<[^>]+>", " ", html.unescape(desc))

                company = ""
                title = raw_title
                if ":" in raw_title:
                    parts = raw_title.split(":", 1)
                    company = parts[0].strip()
                    title = parts[1].strip()

                if url_str:
                    jobs.append(
                        Job(
                            title=title,
                            company=company,
                            url=url_str.strip(),
                            source="WeWorkRemotely",
                            location=location.strip(),
                            description=desc_clean.strip(),
                        )
                    )
    except Exception as e:
        print(f"Aviso al scrapear WeWorkRemotely: {e}")

    return jobs
