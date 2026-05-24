import os
import csv

def export_jobs(jobs):

    folder = "output"

    os.makedirs(folder, exist_ok=True)

    base_name = "new_jobs"
    extension = ".csv"

    counter = 0

    while True:

        if counter == 0:
            filename = f"{base_name}{extension}"
        else:
            filename = f"{base_name}({counter}){extension}"

        path = os.path.join(folder, filename)

        if not os.path.exists(path):
            break

        counter += 1

    with open(path, "w", newline="", encoding="utf-8") as f:

        writer = csv.writer(f)

        writer.writerow([
            "Position",
            "Company",
            "URL",
            "Source",
            "Score",
        ])

        for job in jobs:

            writer.writerow([
                job.title,
                job.company,
                job.url,
                job.source,
                job.score,
            ])

    print(f"CSV exportado: {filename}")