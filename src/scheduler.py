import schedule
import time
import logging
from main import run_pipeline

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def job():
    """Scheduled job to run the pipeline."""
    logger.info("Running scheduled pipeline")
    try:
        run_pipeline()
    except Exception as e:
        logger.error(f"Scheduled pipeline failed: {e}")

if __name__ == "__main__":
    # Schedule to run daily at 2 AM
    schedule.every().day.at("02:00").do(job)

    logger.info("Scheduler started. Running daily at 02:00")
    while True:
        schedule.run_pending()
        time.sleep(60)  # Check every minute