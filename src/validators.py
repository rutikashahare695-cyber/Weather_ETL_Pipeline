"""
Data Validation and Quality Assurance Module.

Implements boundary and type sanity checks on raw API telemetry data
prior to loading it into persistent database storage.
"""

import logging
from typing import Tuple, Dict, Any, Optional

logger = logging.getLogger(__name__)


def validate_weather_record(record: Optional[Dict[str, Any]]) -> Tuple[bool, str]:
    """
    Validates physical plausibility and completeness of extracted weather readings.

    Args:
        record (Optional[Dict[str, Any]]): Extracted dictionary payload.

    Returns:
        Tuple[bool, str]: (Validation result boolean, Descriptive status message)
    """
    # 1. Existence check
    if not record:
        return False, "Validation Failed: Record payload is empty or None."

    # 2. Extract values safely
    temp = record.get('temperature')
    humidity = record.get('humidity')
    pressure = record.get('pressure')

    # 3. Temperature Range Check (-90.0°C to 60.0°C)
    if temp is None or not isinstance(temp, (int, float)):
        return False, f"Validation Failed: Invalid temperature datatype ({temp})."
    if not (-90.0 <= temp <= 60.0):
        return False, f"Validation Failed: Temperature {temp}°C out of realistic range."

    # 4. Relative Humidity Range Check (0% to 100%)
    if humidity is None or not isinstance(humidity, (int, float)):
        return False, f"Validation Failed: Invalid humidity datatype ({humidity})."
    if not (0 <= humidity <= 100):
        return False, f"Validation Failed: Humidity {humidity}% out of 0-100% bounds."

    # 5. Atmospheric Pressure Range Check (800 hPa to 1100 hPa)
    if pressure is None or not isinstance(pressure, (int, float)):
        return False, f"Validation Failed: Invalid pressure datatype ({pressure})."
    if not (800 <= pressure <= 1100):
        return False, f"Validation Failed: Barometric pressure {pressure} hPa physically improbable."

    return True, "Validation Passed: Record satisfies all data quality rules."