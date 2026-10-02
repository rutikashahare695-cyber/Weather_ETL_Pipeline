"""
Database Management Module.

Handles relational database schema creation, connection pooling setup,
and reference data seeding using SQLite.
"""

import sqlite3
import logging
import os
import sys
from typing import List, Dict, Any

# Ensure project root is accessible in import path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config.config import DB_PATH

logger = logging.getLogger(__name__)


def get_connection() -> sqlite3.Connection:
    """
    Establishes and returns a connection to the SQLite database.
    Enforces foreign key constraints for relational integrity.
    
    Returns:
        sqlite3.Connection: Active SQLite connection object.
    """
    conn = sqlite3.connect(DB_PATH)
    # Enable foreign key verification in SQLite (disabled by default)
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn


def setup_database() -> None:
    """
    Initializes the database schema with three normalized tables:
    1. cities: Dimension table storing location metadata.
    2. weather_data: Fact table storing time-series weather readings.
    3. pipeline_logs: Audit table tracking ETL pipeline run status.
    """
    conn = get_connection()
    cursor = conn.cursor()
    
    try:
        # Table 1: Dimension table for cities
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS cities (
                city_id INTEGER PRIMARY KEY AUTOINCREMENT,
                city_name TEXT NOT NULL UNIQUE,
                country TEXT NOT NULL,
                latitude REAL,
                longitude REAL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Table 2: Fact table for time-series weather readings
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS weather_data (
                record_id INTEGER PRIMARY KEY AUTOINCREMENT,
                city_id INTEGER NOT NULL,
                timestamp TIMESTAMP NOT NULL,
                temperature_c REAL NOT NULL,
                humidity INTEGER NOT NULL,
                pressure_hpa REAL,
                wind_speed_mps REAL,
                weather_condition TEXT,
                FOREIGN KEY (city_id) REFERENCES cities (city_id) ON DELETE CASCADE
            )
        ''')
        
        # Table 3: Operational monitoring log table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS pipeline_logs (
                log_id INTEGER PRIMARY KEY AUTOINCREMENT,
                run_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                status TEXT NOT NULL,
                records_processed INTEGER DEFAULT 0,
                error_message TEXT
            )
        ''')
        
        conn.commit()
        logger.info("Database schema initialized successfully.")
    except sqlite3.Error as err:
        logger.error(f"Failed to set up database schema: {err}")
        conn.rollback()
        raise err
    finally:
        conn.close()


def seed_cities(cities_list: List[Dict[str, Any]]) -> None:
    """
    Populates the 'cities' table with initial dimension metadata.
    Ignores entries that already exist to prevent duplicate errors.

    Args:
        cities_list (List[Dict[str, Any]]): List of city dictionaries with coordinates.
    """
    conn = get_connection()
    cursor = conn.cursor()
    
    try:
        for city in cities_list:
            cursor.execute('''
                INSERT OR IGNORE INTO cities (city_name, country, latitude, longitude)
                VALUES (?, ?, ?, ?)
            ''', (city['name'], city['country'], city['lat'], city['lon']))
            
        conn.commit()
        logger.info(f"Successfully seeded {len(cities_list)} target cities into dimension table.")
    except sqlite3.Error as err:
        logger.error(f"Error seeding cities table: {err}")
        conn.rollback()
    finally:
        conn.close()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    setup_database()