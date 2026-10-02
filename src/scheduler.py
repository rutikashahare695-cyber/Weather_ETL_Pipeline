"""
Automated Job Scheduler Module.

Executes the ETL pipeline and reporting functions at periodic intervals.
"""

import schedule
import time
import logging
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.etl_pipeline import run_etl_pipeline
from src.reporter import generate_weather_report

logger = logging.getLogger("Scheduler")


def scheduled_job():
    """
    Callback function executed by scheduler to run ETL and regenerate reports.
    """
    logger.info("Executing scheduled ETL and reporting workflow...")
    run_etl_pipeline()
    generate_weather_report()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    print("🚀 Weather Data Pipeline Scheduler Started.")
    
    # Run once immediately on launch
    scheduled_job()
    
    # Schedule to trigger every 1 hour
    schedule.every(1).hours.do(scheduled_job)
    
    print("⏳ Scheduler active. Running every hour... (Press Ctrl+C to terminate)")
    try:
        while True:
            schedule.run_pending()
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n🛑 Scheduler stopped by user.")