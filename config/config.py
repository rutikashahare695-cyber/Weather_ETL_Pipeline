"""
Configuration Settings Module.

This module centralizes all system parameters, path resolution, API endpoints,
and data quality thresholds used across the Weather Data Pipeline.
"""

import os
from typing import List, Dict, Any

# ==========================================
# PATH CONFIGURATION
# ==========================================
# Dynamically calculate the root directory of the project
BASE_DIR: str = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Paths for database, logs, and generated analytical reports
DB_PATH: str = os.path.join(BASE_DIR, "database", "weather_data.db")
LOG_PATH: str = os.path.join(BASE_DIR, "logs", "pipeline.log")
REPORT_DIR: str = os.path.join(BASE_DIR, "reports")

# Ensure required runtime directories exist
os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
os.makedirs(os.path.dirname(LOG_PATH), exist_ok=True)
os.makedirs(REPORT_DIR, exist_ok=True)


# ==========================================
# API CONFIGURATION (OpenWeatherMap)
# ==========================================
# Retrieve API key from environment variables or fallback to placeholder
API_KEY: str = os.getenv("OPENWEATHER_API_KEY", "YOUR_OPENWEATHERMAP_API_KEY")
BASE_URL: str = "http://api.openweathermap.org/data/2.5/weather"


# ==========================================
# TARGET MONITORING CITIES
# ==========================================
# List of primary Indian urban hubs selected for real-time telemetry extraction
DEFAULT_CITIES: List[Dict[str, Any]] = [
    {"name": "Mumbai", "country": "IN", "lat": 19.0760, "lon": 72.8777},
    {"name": "Delhi", "country": "IN", "lat": 28.6139, "lon": 77.2090},
    {"name": "Bangalore", "country": "IN", "lat": 12.9716, "lon": 77.5946},
    {"name": "Chennai", "country": "IN", "lat": 13.0827, "lon": 80.2707},
    {"name": "Kolkata", "country": "IN", "lat": 22.5726, "lon": 88.3639},
    {"name": "Hyderabad", "country": "IN", "lat": 17.3850, "lon": 78.4867}
]


# ==========================================
# DATA QUALITY & ALERT THRESHOLDS
# ==========================================
# Operational boundaries used by validation and alerting modules
TEMP_HIGH_THRESHOLD: float = 30.0    # Celsius: Triggers heat alert above 30°C
HUMIDITY_HIGH_THRESHOLD: float = 75.0 # Percentage: Triggers high humidity alert above 75%