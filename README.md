# Automotive Telemetry Data Pipeline (ETL)

An automated Extract, Transform, Load (ETL) pipeline in Python that processes vehicle telemetry and IoT sensor streams. It validates and filters sensor anomalies, computes aggregated trip performance metrics, and loads clean data into a relational SQL database.

## Architecture & Flow
1. **Extract (`src/extract.py`)**: Ingests raw telemetry events (speed, battery, engine temperature, timestamp).
2. **Transform (`src/transform.py`)**:
   - Drops records with missing values.
   - Filters domain-specific sensor outliers (negative speeds, values > 250 km/h, out-of-range battery levels).
   - Computes aggregated vehicle metrics (average speed, maximum speed, minimum battery).
3. **Load (`src/load.py`)**: Manages the relational SQL schema and persists both granular events and aggregate summaries into SQLite tables.

## Tech Stack
- **Language**: Python 3.x (Standard Library)
- **Database**: SQL / SQLite
- **Architecture**: Modular ETL Pipeline
- **Version Control**: Git / GitHub

## Running the Project
```bash
python main.py