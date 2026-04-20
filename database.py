import psycopg2
from psycopg2.extras import execute_values
import os
from dotenv import load_dotenv
import logging

load_dotenv()

def get_db_connection():
    db_url = os.getenv("DATABASE_URL")
    if db_url:
        return psycopg2.connect(db_url)
    return psycopg2.connect(
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT")
    )

def init_db():
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        with open('schema.sql', 'r') as f:
            cur.execute(f.read())
        conn.commit()
        cur.close()
        conn.close()
        logging.info("Database initialized successfully.")
    except Exception as e:
        logging.error(f"Error initializing database: {e}")

def save_job(job_data):
    """
    Saves a job and its associated skills to the database.
    job_data keys: title, company, location, salary_min, salary_max, description, posted_at, source_url, skills
    """
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        # Insert job
        cur.execute("""
            INSERT INTO jobs (title, company, location, salary_min, salary_max, description, posted_at, source_url)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (source_url) DO NOTHING
            RETURNING id;
        """, (
            job_data['title'], job_data['company'], job_data['location'],
            job_data['salary_min'], job_data['salary_max'], job_data['description'],
            job_data['posted_at'], job_data['source_url']
        ))
        
        result = cur.fetchone()
        if result:
            job_id = result[0]
            # Link skills
            if job_data['skills']:
                # Get skill IDs
                cur.execute("SELECT id, name FROM skills WHERE name = ANY(%s)", (job_data['skills'],))
                skill_id_map = {name: id for id, name in cur.fetchall()}
                
                skill_links = [(job_id, skill_id_map[skill]) for skill in job_data['skills'] if skill in skill_id_map]
                if skill_links:
                    execute_values(cur, "INSERT INTO job_skills (job_id, skill_id) VALUES %s ON CONFLICT DO NOTHING", skill_links)
        
        conn.commit()
    except Exception as e:
        conn.rollback()
        logging.error(f"Error saving job {job_data.get('source_url')}: {e}")
    finally:
        cur.close()
        conn.close()
