import os
import logging
from datetime import datetime
from dotenv import load_dotenv
from apscheduler.schedulers.blocking import BlockingScheduler
from database import init_db, save_job
from scraper import fetch_remoteok, fetch_adzuna

load_dotenv()

# Configure Logging
logging.basicConfig(
    filename=os.getenv("LOG_FILE", "scraper.log"),
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def run_scraper():
    logging.info("Starting scrape cycle...")
    print(f"[{datetime.now()}] Starting scrape cycle...")
    
    # Fetch jobs
    remoteok_jobs = fetch_remoteok()
    adzuna_jobs = fetch_adzuna()
    
    all_jobs = remoteok_jobs + adzuna_jobs
    
    logging.info(f"Fetched {len(all_jobs)} total jobs. Saving to database...")
    print(f"Saving {len(all_jobs)} jobs to database...")
    
    # Save to DB
    for job in all_jobs:
        save_job(job)
        
    logging.info("Scrape cycle completed.")
    print(f"[{datetime.now()}] Scrape cycle completed.")

if __name__ == "__main__":
    # Initialize Database
    init_db()
    
    # Run once immediately
    run_scraper()
    
    # Setup Scheduler
    interval_hours = int(os.getenv("SCRAPE_INTERVAL_HOURS", 24))
    scheduler = BlockingScheduler()
    scheduler.add_job(run_scraper, 'interval', hours=interval_hours)
    
    logging.info(f"Scheduler started. Running every {interval_hours} hours.")
    print(f"Scheduler started. Running every {interval_hours} hours. Press Ctrl+C to exit.")
    
    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        logging.info("Scheduler stopped.")
        print("\nScheduler stopped.")
