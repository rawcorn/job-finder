# Job Finder

Remote job scraping bot that automatically collects, filters, scores, and exports new remote jobs from multiple job boards, with automatic XLSX export.

## Supported Websites

- RemoteOK
- Remotive
- DynamiteJobs
- Jobspresso
- NoDesk
- WeWorkRemotely
- WorkingNomads

## Features

- Multi-site job scraping
- Keyword-based filtering
- Easy Apply detection
- Duplicate prevention with SQLite
- Job scoring and ranking
- CSV export
- Persistent local database
- Playwright-powered scraping for JS-heavy websites

## Requirements

```bash
pip install -r requirements.txt
playwright install
```

## Run

```bash
python main.py
```

## Output

New jobs are automatically exported to:

```text
output/
```

Each execution generates a new CSV file containing only newly discovered jobs.

Example:

```text
new_jobs.xlsx
new_jobs(1).xlsx
new_jobs(2).xlsx
```

## Database

```text
jobs.db
```

Stores previously processed job URLs to prevent duplicates across executions.

## Filters

Filtering logic is located in:

```text
filters.py
```

Includes:
- keyword filtering
- regional filtering (Argentina, LATAM, worldwide, etc.)
- easy apply detection
- relevance filtering
- job scoring

## Configuration

Editable keywords are configured in:

```text
config.py
```

## Project Structure

```text
job_finder/
│
├── output/
├── scrapers/
├── main.py
├── filters.py
├── database.py
├── exporter.py
├── config.py
├── models.py
├── requirements.txt
├── README.md
└── .gitignore
```