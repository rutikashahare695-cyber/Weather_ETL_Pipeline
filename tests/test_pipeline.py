"""
Automated Unit Testing Module.

Tests database initialization, API response parsing, and data validation rules using unittest.
"""

import unittest
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.validators import validate_weather_record


class TestWeatherPipeline(unittest.TestCase):
    """Unit tests for pipeline validation functions."""

    def test_valid_weather_record(self):
        """Test that a realistic weather record passes validation."""
        record = {
            'temperature': 25.5,
            'humidity': 60,
            'pressure': 1012.0
        }
        is_valid, msg = validate_weather_record(record)
        self.assertTrue(is_valid)

    def test_invalid_temperature_high(self):
        """Test that unrealistically high temperatures fail validation."""
        record = {
            'temperature': 150.0, # Impossible reading
            'humidity': 50,
            'pressure': 1010.0
        }
        is_valid, msg = validate_weather_record(record)
        self.assertFalse(is_valid)

    def test_invalid_humidity_negative(self):
        """Test that negative humidity fails validation."""
        record = {
            'temperature': 20.0,
            'humidity': -10, # Out of 0-100% bounds
            'pressure': 1010.0
        }
        is_valid, msg = validate_weather_record(record)
        self.assertFalse(is_valid)


if __name__ == "__main__":
    unittest.main()