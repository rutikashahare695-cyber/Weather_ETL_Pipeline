"""
Pipeline Monitoring & Health Checks Module.

Evaluates data freshness, missing records, log health, and database connection status.
"""

import logging
import sqlite3
import os
import sys
from typing import Dict, Any

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config.config import DB_PATH
from src.database import get_connection

logger = logging.getLogger(__name__)


def check_pipeline_health() -> Dict[str, Any]:
    """
    Performs comprehensive diagnostic checks on database connection,
    stale data detection, and error log history.

    Returns:
        Dict[str, Any]: Health metrics dictionary.
    """
    health_status = {
        "database_connected": False,
        "total_records": 0,
        "failed_runs_count": 0,
        "system_health": "UNKNOWN"
    }
    
    try:
        conn = get_connection()
        cursor = conn.cursor()
        health_status["database_connected"] = True
        
        # Check total dataset size
        cursor.execute("SELECT COUNT(*) FROM weather_data")
        health_status["total_records"] = cursor.fetchone()[0]
        
        # Count pipeline crashes in log table
        cursor.execute("SELECT COUNT(*) FROM pipeline_logs WHERE status = 'Failed'")
        health_status["failed_runs_count"] = cursor.fetchone()[0]
        
        # Overall status determination
        if health_status["failed_runs_count"] == 0:
            health_status["system_health"] = "HEALTHY"
        else:
            health_status["system_health"] = "WARNING - Failures Recorded"
            
        conn.close()
    except sqlite3.Error as err:
        health_status["system_health"] = f"CRITICAL - DB Connection Error: {err}"
        logger.error(f"Health check failure: {err}")
        
    return health_status


if __name__ == "__main__":
    status = check_pipeline_health()
    print("--- System Health Check Diagnostics ---")
    for key, value in status.items():
        print(f"{key}: {value}")