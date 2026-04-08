import sqlite3
import os
from datetime import datetime, timedelta

DB_PATH = os.path.join(os.path.dirname(__file__), "jobs.db")


def get_connection():
    return sqlite3.connect(DB_PATH)


def create_table():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS jobs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        company TEXT,
        location TEXT,
        link TEXT,
        description TEXT,
        source TEXT,
        created_at TIMESTAMP,
        embedded INTEGER DEFAULT 0
    )
    """)

    conn.commit()
    conn.close()


def delete_old_jobs(hours=72):
    conn = get_connection()
    cursor = conn.cursor()

    threshold = datetime.utcnow() - timedelta(hours=hours)

    cursor.execute("""
    DELETE FROM jobs WHERE created_at < ?
    """, (threshold,))

    deleted = cursor.rowcount

    conn.commit()
    conn.close()

    print(f"🗑️ Deleted {deleted} old jobs (> {hours} hrs)")


def insert_jobs(jobs):
    conn = get_connection()
    cursor = conn.cursor()

    inserted = 0

    for job in jobs:
        title = job.get("title", "")
        company = job.get("company", "")
        location = job.get("location", "")

        if not title or not company:
            continue

        # Dedup check
        cursor.execute("""
        SELECT id FROM jobs
        WHERE title=? AND company=? AND location=?
        """, (title, company, location))

        if cursor.fetchone():
            continue

        cursor.execute("""
        INSERT INTO jobs (title, company, location, link, description, source, created_at, embedded)
        VALUES (?, ?, ?, ?, ?, ?, ?, 0)
        """, (
            title,
            company,
            location,
            job.get("job_url") or job.get("link", ""),
            job.get("description", ""),
            job.get("site", ""),
            datetime.utcnow()
        ))

        inserted += 1

    conn.commit()
    conn.close()

    print(f"🆕 Inserted {inserted} new jobs")


def fetch_unembedded_jobs():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT id, title, company, location, link, description
    FROM jobs
    WHERE embedded = 0
    """)

    rows = cursor.fetchall()
    conn.close()

    jobs = []
    for r in rows:
        jobs.append({
            "id": r[0],
            "title": r[1],
            "company": r[2],
            "location": r[3],
            "link": r[4],
            "description": r[5],
        })

    print(f"🆕 {len(jobs)} new jobs to embed")
    return jobs


def mark_jobs_embedded(job_ids):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.executemany(
        "UPDATE jobs SET embedded = 1 WHERE id = ?",
        [(jid,) for jid in job_ids]
    )

    conn.commit()
    conn.close()