import sqlite3
from models import Job

DB_PATH = "jobs.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS jobs (
            url TEXT PRIMARY KEY,
            title TEXT,
            company TEXT,
            source TEXT,
            location TEXT,
            easy_apply INTEGER,
            score INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.commit()
    conn.close()


def save_job(job: Job) -> bool:
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    try:
        cur.execute("""
            INSERT INTO jobs (
                url,
                title,
                company,
                source,
                location,
                easy_apply,
                score
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            job.url,
            job.title,
            job.company,
            job.source,
            job.location,
            int(job.easy_apply),
            job.score,
        ))

        inserted = cur.rowcount == 1
        conn.commit()
        return inserted

    except sqlite3.IntegrityError:
        conn.rollback()
        return False

    finally:
        conn.close()