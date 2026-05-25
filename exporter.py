import os
from openpyxl import Workbook
from openpyxl.styles import Font


def export_jobs(jobs):

    folder = os.path.join(os.path.expanduser("~"), "Desktop", "JOBLIST")

    os.makedirs(folder, exist_ok=True)

    base_name = "new_jobs"
    extension = ".xlsx"

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

    wb = Workbook()
    ws = wb.active

    ws.title = "Jobs"

    headers = [
        "Position",
        "Company",
        "URL",
        "Source",
        "Score",
    ]

    ws.append(headers)

    # Headers en bold
    for cell in ws[1]:
        cell.font = Font(bold=True)

    for job in jobs:

        ws.append([
            job.title,
            job.company,
            job.url,
            job.source,
            job.score,
        ])

        row = ws.max_row

        # Hyperlink clickeable
        ws.cell(row=row, column=3).hyperlink = job.url
        ws.cell(row=row, column=3).style = "Hyperlink"

    # Ajustar ancho columnas
    column_widths = {
        "A": 45,
        "B": 30,
        "C": 70,
        "D": 25,
        "E": 10,
    }

    for col, width in column_widths.items():
        ws.column_dimensions[col].width = width

    wb.save(path)

    print(f"XLSX exportado: {path}")