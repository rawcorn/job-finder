from config import KEYWORDS
from models import Job


EXCLUDE_TERMS = [
    "us only",
    "united states only",
    "must reside in the us",
    "on-site",
    "onsite",
]

PREFERRED_TERMS = [
    "argentina",
    "argentinian",
    "latam",
    "latin america",
    "south america",
    "worldwide",
    "americas",
]


def is_relevant(job: Job) -> bool:
    text = f"{job.title} {job.description} {job.location}".lower()


    if not any(keyword in text for keyword in KEYWORDS):
        return False


    if any(term in text for term in EXCLUDE_TERMS):
        return False

    return True


def detect_easy_apply(job: Job) -> bool:
    url = job.url.lower()

    easy_domains = [
        "greenhouse.io",
        "boards.greenhouse.io",
        "lever.co",
        "jobs.lever.co",
        "ashbyhq.com",
        "workable.com",
        "bamboohr.com",
    ]

    return any(domain in url for domain in easy_domains)


def calculate_score(job: Job) -> int:
    score = 0
    text = f"{job.title} {job.description} {job.location}".lower()

    if detect_easy_apply(job):
        score += 20

    for term in PREFERRED_TERMS:
        if term in text:
            score += 20
            break

    if "remote" in text:
        score += 10

    return score