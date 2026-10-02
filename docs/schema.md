# Database Schema Documentation

## Entity Relationship Summary
The weather database (`weather_data.db`) consists of 3 normalized tables:

1. **`cities` (Dimension Table)**: Stores unique geographic locations.
2. **`weather_data` (Fact Table)**: Stores time-series weather observation data linked to cities via Foreign Key (`city_id`).
3. **`pipeline_logs` (Audit Table)**: Tracks ETL pipeline execution metrics, timing, status, and error logs.

---

## Data Dictionaries

### 1. `cities` Table
| Column Name | Data Type | Constraints | Description |
|---|---|---|---|
| `city_id` | INTEGER | PRIMARY KEY AUTOINCREMENT | Unique identifier for each city |
| `city_name` | TEXT | NOT NULL, UNIQUE | Name of the city (e.g., Mumbai) |
| `country` | TEXT | NOT NULL | Country code (e.g., IN) |
| `latitude` | REAL | - | Latitude coordinate |
| `longitude` | REAL | - | Longitude coordinate |
| `created_at` | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | Timestamp when record was created |

### 2. `weather_data` Table
| Column Name | Data Type | Constraints | Description |
|---|---|---|---|
| `record_id` | INTEGER | PRIMARY KEY AUTOINCREMENT | Unique observation ID |
| `city_id` | INTEGER | FOREIGN KEY REFERENCES `cities(city_id)` | Link to city record |
| `timestamp` | TIMESTAMP | NOT NULL | Time of weather measurement |
| `temperature_c` | REAL | NOT NULL | Temperature in Celsius |
| `humidity` | INTEGER | NOT NULL | Relative humidity percentage |
| `pressure_hpa` | REAL | - | Barometric pressure in hPa |
| `wind_speed_mps` | REAL | - | Wind speed in meters per second |
| `weather_condition` | TEXT | - | Sky condition (e.g., Clear sky) |

### 3. `pipeline_logs` Table
| Column Name | Data Type | Constraints | Description |
|---|---|---|---|
| `log_id` | INTEGER | PRIMARY KEY AUTOINCREMENT | Unique execution log ID |
| `run_timestamp` | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | Pipeline run execution time |
| `status` | TEXT | NOT NULL | Run outcome (`Successful`, `Failed`, `Warning`) |
| `records_processed` | INTEGER | DEFAULT 0 | Count of records loaded into DB |
| `error_message` | TEXT | - | Exception details if run failed |