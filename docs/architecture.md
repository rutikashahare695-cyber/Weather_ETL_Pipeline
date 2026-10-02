# Weather Data Pipeline System - Architecture & Technical Documentation

This document outlines the system architecture, design patterns, data flow, and SQL analytical framework for the Weather Data Pipeline System.

---

## 1. System Overview & Architecture Diagram

The system follows a modular, layer-separated Data Engineering architecture designed around the Extract, Transform, Load (ETL) pattern.

```text
               ┌────────────────────────┐
               │ OpenWeatherMap REST API│
               └───────────┬───────────s─┘
                           │
                           │ 1. Extract (HTTP GET)
                           ▼
               ┌────────────────────────┐
               │    src/api_client.py   │
               └───────────┬────────────┘
                           │
                           │ 2. Raw Telemetry Payload
                           ▼
               ┌────────────────────────┐
               │    src/validators.py   │
               └───────────┬────────────┘
                           │
                           │ 3. Data Integrity & Boundary Checks
                           ▼
               ┌────────────────────────┐
               │  src/etl_pipeline.py   │
               └───────────┬────────────┘
                           │
                           │ 4. Structured Records & Logs
                           ▼
      ┌──────────────────────────────────────────┐
      │     SQLite Database (weather_data.db)    │
      │ ┌──────────────┬──────────────┬────────┐ │
      │ │    cities    │ weather_data │  logs  │ │
      │ └──────────────┴──────────────┴────────┘ │
      └────────────────────┬─────────────────────┘
                           │
                           │ 5. SQL Analytics Queries
                           ▼
               ┌────────────────────────┐
               │    src/reporter.py     │
               └───────────┬────────────┘
                           │
                           │ 6. Generated Reports & Alerts
                           ▼
              ┌──────────────────────────┐
              │ reports/summary_report.txt│
              └──────────────────────────┘
```

# 2. Core Components Breakdown
## 2.1 Extraction Layer (src/api_client.py)
API Source: OpenWeatherMap REST API (/data/2.5/weather endpoint).
Communication Protocol: HTTP GET requests with structured query parameters (units=metric).
Resilience: Configured with a 10-second timeout mechanism, response status code verification (raise_for_status()), and explicit exception handling for timeouts, network drops, and HTTP client/server errors.

## 2.2 Data Quality & Validation Layer (src/validators.py)
Executes pre-ingestion checks to ensure physical realism of metrics before persistent storage:
   Temperature Check: Validates values within physical boundaries ($-90.0^\circ\text{C} \le T \le 60.0^\circ\text{C}$).
   Humidity Check: Ensures relative humidity remains within legal percentages ($0\% \le H \le 100\%$).Pressure Check: Confirms barometric pressure falls within reasonable atmospheric limits ($800\text{ hPa} \le P \le 1100\text{ hPa}$).
   Data Type Verification: Ensures numeric parameters are valid floats or integers.

## 2.3 Orchestration & Database Engine (src/etl_pipeline.py & src/database.py)
Database: SQLite persistent storage.
Relational Design: Schema normalized to Third Normal Form (3NF) containing:
   cities (Dimension Table): Master metadata for monitored locations.
   weather_data (Fact Table): Time-series metrics indexed by foreign keys.
   pipeline_logs (Audit Table): Tracks system execution health, throughput, and exceptions.
Transactional Safety: Uses explicit database transactions (commit/rollback) to ensure data atomicity during ingestion.

## 2.4 Analytical Reporting & Monitoring Layer (src/reporter.py & src/monitor.py)
Formats metrics into human-readable daily summaries.
Evaluates operational alert rules ($T > 30.0^\circ\text{C}$ and Humidity $> 75\%$).
Monitors database state, log integrity, and system health status.

# 3. SQL Analytics Framework & Problem Solutions
Below are the SQL queries designed to answer key analytical business questions on historical weather observations stored in the system.

Question 1: Which city has the highest average temperature?

SQL
SELECT 
    c.city_name,
    c.country,
    ROUND(AVG(w.temperature_c), 2) AS avg_temperature_c
FROM weather_data w
JOIN cities c ON w.city_id = c.city_id
GROUP BY c.city_id, c.city_name, c.country
ORDER BY avg_temperature_c DESC
LIMIT 1;

Question 2: What are the temperature trends over the last 30 days?

SQL
SELECT 
    DATE(w.timestamp) AS observation_date,
    c.city_name,
    ROUND(AVG(w.temperature_c), 2) AS daily_avg_temp,
    ROUND(MIN(w.temperature_c), 2) AS daily_min_temp,
    ROUND(MAX(w.temperature_c), 2) AS daily_max_temp
FROM weather_data w
JOIN cities c ON w.city_id = c.city_id
WHERE w.timestamp >= DATE('now', '-30 days')
GROUP BY DATE(w.timestamp), c.city_id, c.city_name
ORDER BY observation_date ASC, c.city_name ASC;

Question 3: How does humidity correlate with weather conditions?

SQL
SELECT 
    w.weather_condition,
    COUNT(*) AS total_observations,
    ROUND(AVG(w.humidity), 2) AS avg_humidity_pct,
    ROUND(MIN(w.humidity), 2) AS min_humidity_pct,
    ROUND(MAX(w.humidity), 2) AS max_humidity_pct
FROM weather_data w
GROUP BY w.weather_condition
ORDER BY avg_humidity_pct DESC;

Question 4: What are the peak temperature hours for each city?

SQL
WITH HourlyAverages AS (
    SELECT 
        c.city_name,
        STRFTIME('%H:00', w.timestamp) AS hour_of_day,
        ROUND(AVG(w.temperature_c), 2) AS avg_temp,
        DENSE_RANK() OVER (
            PARTITION BY c.city_id 
            ORDER BY AVG(w.temperature_c) DESC
        ) AS rank_order
    FROM weather_data w
    JOIN cities c ON w.city_id = c.city_id
    GROUP BY c.city_id, c.city_name, hour_of_day
)
SELECT 
    city_name,
    hour_of_day AS peak_hour,
    avg_temp AS peak_avg_temperature
FROM HourlyAverages
WHERE rank_order = 1
ORDER BY city_name ASC;
# 4. Operational Monitoring & Security Considerations
Error Handling & Logging: All pipeline failures append structured exception records to logs/pipeline.log as well as the pipeline_logs database table.
Key Security: API authentication keys are retrieved dynamically via environment variables (OPENWEATHER_API_KEY) to prevent credential leaks in version control repositories.
Database Integrity: Foreign key constraints are explicitly enabled (PRAGMA foreign_keys = ON;) to protect relational table connections.