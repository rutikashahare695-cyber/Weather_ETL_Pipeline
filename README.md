# Weather Data Pipeline System 🌤️📊

An end-to-end Data Engineering pipeline built using Python and SQLite. This system automatically extracts real-time weather observations via the OpenWeatherMap REST API, validates measurement integrity, transforms payloads, loads structured records into a normalized SQL database, and generates automated summary reports and operational alerts.

---

## 🌟 Key Features

- **REST API Integration**: Built-in API client with error handling, custom timeouts, HTTP status validation, and exception logging.
- **Normalized SQLite Database**: 3NF schema containing dimension (`cities`), fact (`weather_data`), and audit logging (`pipeline_logs`) tables.
- **Data Quality & Validation**: Automated pre-ingestion bounds checking for temperature, humidity, and barometric pressure physical limits.
- **Automated Scheduling**: Scheduled background ETL workflow execution using Python's `schedule` library.
- **Analytical Reporting**: Automated textual snapshot generation, database statistics, and threshold-based weather alerts.
- **Monitoring & Health Checks**: Integrated diagnostics for pipeline execution history, log health, and database connectivity.

---

## 📁 Repository Structure

```text
weather-etl-pipeline/
│
├── README.md               # Complete system documentation & setup guide
├── requirements.txt        # Python dependency manifest
│
├── config/
│   └── config.py          # Centralized pathing, API, and threshold configuration
│
├── src/
│   ├── __init__.py
│   ├── database.py        # SQLite schema setup, connections, and dimension seeding
│   ├── api_client.py      # OpenWeatherMap API extraction logic
│   ├── validators.py      # Data quality and sanity checking functions
│   ├── etl_pipeline.py    # Core Extract-Transform-Load engine
│   ├── reporter.py        # Analytical report and alert generator
│   ├── monitor.py         # System health check diagnostics
│   └── scheduler.py       # Automated job execution scheduler
│
├── database/
│   └── weather_data.db    # Persistent SQLite relational database
│
├── tests/
│   └── test_pipeline.py   # Automated unit test suite using unittest
│
├── docs/
│   ├── architecture.md    # System architecture, data flow, and SQL query solutions
│   └── schema.md          # Database schema dictionaries and entity relationships
│
├── logs/
│   └── pipeline.log       # Persistent execution log history
│
└── reports/
    └── summary_report.txt # Output analytical summary reports
```

# ⚙️ Environment Setup & Installation
1. Prerequisites
Ensure you have Python 3.8 or higher installed on your system.

2. Install Dependencies
Install all required Python packages using requirements.txt:

Bash
pip install -r requirements.txt

3. API Key Configuration
Set your OpenWeatherMap API key as an environment variable (recommended):

On Linux/macOS:

Bash
export OPENWEATHER_API_KEY="your_api_key_here"
On Windows (Command Prompt):

DOS
set OPENWEATHER_API_KEY=your_api_key_here
(Note: If no environment variable is set, the pipeline will fallback to the key defined in config/config.py)

# 🚀 Usage & Execution Guide
## Step 1: Run Unit Tests
Verify data validation rules and system functions before running the pipeline:

Bash
python tests/test_pipeline.py
## Step 2: Execute the ETL Pipeline
Extract real-time weather metrics, perform transformations, and load data into SQLite:

Bash
python src/etl_pipeline.py
## Step 3: Generate Weather Report & Alerts
Compile system metrics and generate the analytical report in reports/summary_report.txt:

Bash
python src/reporter.py
## Step 4: Run System Health Check
Check database connection status, error logs, and total record count:

Bash
python src/monitor.py
## Step 5: Start Automated Scheduler (Optional)
Run the pipeline automatically at 1-hour periodic intervals:

Bash
python src/scheduler.py

# 📊 Sample Report Output
When you run python src/reporter.py, the generated output matches the following structure:

Plaintext
WEATHER DATA PIPELINE SYSTEM
=============================

📊 SYSTEM STATUS: RUNNING
⏰ Last Run: 2026-09-27 16:00:00
✅ Status: Successful
📈 Records Processed: 6 cities

🌤️ CURRENT WEATHER SNAPSHOT:
---------------------------------
📍 Bangalore: 24.8°C, 70% humidity, Light rain
📍 Chennai: 30.2°C, 75% humidity, Clear sky
📍 Delhi: 22.3°C, 45% humidity, Partly cloudy
📍 Hyderabad: 27.1°C, 68% humidity, Overcast clouds
📍 Kolkata: 26.5°C, 80% humidity, Scattered clouds
📍 Mumbai: 28.5°C, 65% humidity, Clear sky

📅 TODAY'S ALERTS:
• High temperature alert: Chennai (30.2°C > 30.0°C threshold)
• High humidity alert: Kolkata (80% > 75% threshold)

📊 DATABASE STATISTICS:
• Total records: 36
• Cities tracked: 6
• Data coverage: 99.5%
• Last error: None

# 🛠️ Tech Stack
Language: Python 3.8+

Database: SQLite3

Libraries: requests, pandas, schedule, unittest

Data Source: OpenWeatherMap API

# 📝 Quality Assurance Checklist
[x] Clear modular repository structure.

[x] Fully commented code with Google-style docstrings and explicit type hints.

[x] Complete database schema normalization (3NF).

[x] Robust error handling for network timeouts and malformed API payloads.

[x] Unit test suite covering data quality rules.

[x] Detailed architectural documentation and SQL analytics queries in docs/.