"""
API Communication Module.

Provides functions to interact with the OpenWeatherMap REST API,
handling network requests, timeouts, and error scenarios gracefully.
"""

import requests
import logging
import os
import sys
from typing import Optional, Dict, Any

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config.config import API_KEY, BASE_URL

logger = logging.getLogger(__name__)


def fetch_weather_data(city_name: str) -> Optional[Dict[str, Any]]:
    """
    Retrieves real-time weather observations for a target city from OpenWeatherMap API.

    Args:
        city_name (str): Name of the target city (e.g., 'Hyderabad').

    Returns:
        Optional[Dict[str, Any]]: Extracted weather payload dict, or None if extraction fails.
    """
    # Define query parameters for metric system conversion (°C, m/s)
    params = {
        'q': city_name,
        'appid': API_KEY,
        'units': 'metric'
    }
    
    try:
        # Issue HTTP GET request with a strict 10-second timeout
        response = requests.get(BASE_URL, params=params, timeout=10)
        
        # Raise HTTPError if response code is 4xx or 5xx
        response.raise_for_status()
        data = response.json()
        
        # Cleanly extract key telemetry fields
        extracted_record = {
            'city_name': city_name,
            'timestamp': data.get('dt'),
            'temperature': data['main']['temp'],
            'humidity': data['main']['humidity'],
            'pressure': data['main']['pressure'],
            'wind_speed': data['wind']['speed'],
            'condition': data['weather'][0]['description'].capitalize()
        }
        
        logger.info(f"Successfully retrieved API weather data for city: {city_name}")
        return extracted_record

    except requests.exceptions.HTTPError as http_err:
        logger.error(f"HTTP Error for '{city_name}': {http_err} (Check API Key validity)")
    except requests.exceptions.Timeout:
        logger.error(f"Request timeout for '{city_name}'. OpenWeatherMap server took too long.")
    except requests.exceptions.RequestException as req_err:
        logger.error(f"Network error fetching weather for '{city_name}': {req_err}")
    except (KeyError, IndexError) as parse_err:
        logger.error(f"Failed to parse JSON response for '{city_name}': Missing key {parse_err}")
        
    return None