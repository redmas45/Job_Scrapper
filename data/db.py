import sqlite3

DB_PATH = "data/jobs.db"


def get_connection():
    return sqlite3.connect(DB_PATH)


# ================================
# ✅ CREATE TABLE
# ================================
def create_table():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS jobs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        company TEXT,
        location TEXT,
        description TEXT,
        link TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    conn.commit()
    conn.close()


# ================================
# ✅ INSERT JOBS
# ================================
def insert_jobs(jobs):
    conn = get_connection()
    cursor = conn.cursor()

    for job in jobs:
        cursor.execute("""
        INSERT INTO jobs (title, company, location, description, link)
        VALUES (?, ?, ?, ?, ?)
        """, (
            job.get("title", ""),
            job.get("company", ""),
            job.get("location", ""),
            job.get("description", ""),
            job.get("link", "")
        ))

    conn.commit()
    conn.close()


# ================================
# ✅ DELETE OLD JOBS (TTL CLEANUP)
# ================================
def delete_old_jobs(hours=72):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(f"""
    DELETE FROM jobs
    WHERE created_at < datetime('now', '-{hours} hours')
    """)

    conn.commit()
    conn.close()


# ================================
# ✅ FETCH ALL JOBS (FOR EMBEDDING)
# ================================
def fetch_all_jobs():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM jobs")
    rows = cursor.fetchall()

    columns = [col[0] for col in cursor.description]

    jobs = []
    for row in rows:
        job = dict(zip(columns, row))

        # Normalize fields
        job["title"] = job.get("title", "")
        job["company"] = job.get("company", "")
        job["location"] = job.get("location", "")
        job["description"] = job.get("description", "")

        jobs.append(job)

    conn.close()
    return jobs