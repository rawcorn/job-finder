from database import init_db, save_job
from filters import is_relevant, detect_easy_apply, calculate_score
from scrapers.remoteok import scrape as scrape_remoteok
from scrapers.remotive import scrape as scrape_remotive
from scrapers.dynamitejobs import scrape as scrape_dynamitejobs
from scrapers.jobspresso import scrape as scrape_jobspresso
from scrapers.nodesk import scrape as scrape_nodesk
from scrapers.weworkremotely import scrape as scrape_weworkremotely
from scrapers.workingnomads import scrape as scrape_workingnomads
from exporter import export_jobs

import os

def main():
    init_db()
    print(os.getcwd())

    all_jobs = []

    print("Scrapeando Remote OK...")
    remoteok_jobs = scrape_remoteok()
    print(f"Remote OK encontró: {len(remoteok_jobs)} jobs")
    all_jobs.extend(remoteok_jobs)

    print("Scrapeando Remotive...")
    remotive_jobs = scrape_remotive()
    print(f"Remotive encontró: {len(remotive_jobs)} jobs")
    all_jobs.extend(remotive_jobs)

    print("Scrapeando Dynamite Jobs...")
    dynamite_jobs = scrape_dynamitejobs()
    print(f"Dynamite Jobs encontró: {len(dynamite_jobs)} jobs")
    all_jobs.extend(dynamite_jobs)

    print("Scrapeando Jobspresso...")
    jobspresso_jobs = scrape_jobspresso()
    print(f"Jobspresso encontró: {len(jobspresso_jobs)} jobs")
    all_jobs.extend(jobspresso_jobs)

    print("Scrapeando Nodesk...")
    nodesk_jobs = scrape_nodesk()
    print(f"Nodesk encontró: {len(nodesk_jobs)} jobs")
    all_jobs.extend(nodesk_jobs)

    print("Scrapeando Weworkremotely...")
    weworkremotely_jobs = scrape_weworkremotely()
    print(f"Weworkremotely encontró: {len(weworkremotely_jobs)} jobs")
    all_jobs.extend(weworkremotely_jobs)

    print("Scrapeando Workingnomads...")
    workingnomads_jobs = scrape_workingnomads()
    print(f"Workingnomads encontró: {len(workingnomads_jobs)} jobs")
    all_jobs.extend(workingnomads_jobs)

    print(f"Total scrapeados: {len(all_jobs)}")

    new_jobs = []
    duplicates = 0
    filtered_out = 0

    for job in all_jobs:
        if not is_relevant(job):
            filtered_out += 1
            continue

        job.easy_apply = detect_easy_apply(job)
        job.score = calculate_score(job)

        if save_job(job):
            new_jobs.append(job)
        else:
            duplicates += 1

    new_jobs.sort(key=lambda x: x.score, reverse=True)

    print(f"NEW JOBS: {len(new_jobs)}")
    if new_jobs:
        export_jobs(new_jobs)
    else:
        print("No hay jobs nuevos.")

    for i, job in enumerate(new_jobs, 1):
        print(f"{i}. {job.title} | {job.company}")
        print(job.url)
        print()

if __name__ == "__main__":
    main()