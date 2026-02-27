from apscheduler.schedulers.asyncio import AsyncIOScheduler
from app.migrate import migrate_data
import logging

logger = logging.getLogger(__name__)

scheduler = AsyncIOScheduler()

def start_worker():
    logger.info("Starting background worker for data synchronization...")
    # Schedule the migration task to run every 15 minutes
    scheduler.add_job(migrate_data, "interval", minutes=15, id="sync_data_job")
    scheduler.start()
    logger.info("Background worker started. Syncing every 15 minutes.")

def stop_worker():
    logger.info("Stopping background worker...")
    scheduler.shutdown()
    logger.info("Background worker stopped.")
