"""
ETL Core Pipeline Orchestrator.

Manages end-to-end Extract, Transform, and Load workflows,
coordinating API clients, data validators, database transactions, and execution logging.
"""

import sqlite3
import logging
from datetime import datetime
import os
import sys
from typing import Tuple

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config.config import DEFAULT_CITIES, LOG_PATH
from src.database import get_connection, setup_database, seed_cities
from src.api_client import fetch_weather_data
from src.validators import validate_weather_record

# Setup persistent logging to file and standard output
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[
        logging.FileHandler(LOG_PATH, mode="a", encoding="utf-8"),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger("ETL_Pipeline")


def run_etl_pipeline() -> Tuple[str, int]:
    """
    Executes one complete iteration of the ETL pipeline:
    - Extract: Fetch live weather telemetry for target cities via API.
    - Transform: Clean, format timestamps, and validate measurement thresholds.
    - Load: Insert validated records into SQLite fact tables and record run status.

    Returns:
        Tuple[str, int]: Pipeline run status ('Successful'/'Failed') and count of records loaded.
    """
    logger.info("=== Starting ETL Pipeline Execution ===")
    
    # Guarantee schema and seed dimensions before starting run
    setup_database()
    seed_cities(DEFAULT_CITIES)
    
    conn = get_connection()
    cursor = conn.cursor()
    
    records_processed: int = 0
    error_message: str = None
    
    try:
        for city_info in DEFAULT_CITIES:
            city_name = city_info['name']
            
            # --- STEP 1: EXTRACT ---
            raw_data = fetch_weather_data(city_name)
            
            # --- STEP 2: TRANSFORM & VALIDATE ---
            is_valid, val_msg = validate_weather_record(raw_data)
            if not is_valid:
                logger.warning(f"Skipping record for '{city_name}': {val_msg}")
                continue
            
            # Convert UNIX timestamp to standard ISO datetime string
            formatted_timestamp = datetime.fromtimestamp(raw_data['timestamp']).strftime('%Y-%m-%d %H:%M:%S')
            
            # Retrieve foreign key reference for city
            cursor.execute("SELECT city_id FROM cities WHERE city_name = ?", (city_name,))
            city_row = cursor.fetchone()
            if not city_row:
                logger.error(f"City '{city_name}' not found in dimension table.")
                continue
            city_id = city_row[0]
            
            # --- STEP 3: LOAD ---
            cursor.execute('''
                INSERT INTO weather_data (
                    city_id, timestamp, temperature_c, humidity, 
                    pressure_hpa, wind_speed_mps, weather_condition
                ) VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (
                city_id,
                formatted_timestamp,
                raw_data['temperature'],
                raw_data['humidity'],
                raw_data['pressure'],
                raw_data['wind_speed'],
                raw_data['condition']
            ))
            records_processed += 1
        
        status = "Successful" if records_processed > 0 else "Warning"

    except Exception as e:
        status = "Failed"
        error_message = str(e)
        logger.critical(f"ETL Execution crashed: {e}", exc_info=True)
    
    # Audit trail: Log pipeline execution metrics to database
    cursor.execute('''
        INSERT INTO pipeline_logs (status, records_processed, error_message)
        VALUES (?, ?, ?)
    ''', (status, records_processed, error_message))
    
    conn.commit()
    conn.close()
    
    logger.info(f"=== ETL Execution Finished. Status: {status} | Processed: {records_processed} ===")
    return status, records_processed


if __name__ == "__main__":
    run_etl_pipeline()