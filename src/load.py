import sqlite3
from typing import List, Dict, Any

def get_database_connection(db_name: str = "telemetry.db"):
    return sqlite3.connect(db_name)

def init_db(conn):
    """
    Initializes relational database tables if they do not exist.
    """
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS vehicle_readings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            vehicle_id TEXT NOT NULL,
            timestamp TEXT NOT NULL,
            speed_kmh REAL NOT NULL,
            battery_pct INTEGER NOT NULL,
            engine_temp_c REAL NOT NULL
        );
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS vehicle_summary (
            vehicle_id TEXT PRIMARY KEY,
            avg_speed REAL,
            max_speed REAL,
            avg_engine_temp REAL,
            min_battery INTEGER,
            readings_count INTEGER
        );
    """)
    conn.commit()

def load_data(readings: List[Dict[str, Any]], summaries: List[Dict[str, Any]], db_name: str = "telemetry.db"):
    """
    Loads normalized raw events and aggregated summaries into the SQL database.
    """
    conn = get_database_connection(db_name)
    init_db(conn)
    cursor = conn.cursor()

    # Load clean telemetry rows
    for r in readings:
        cursor.execute("""
            INSERT INTO vehicle_readings (vehicle_id, timestamp, speed_kmh, battery_pct, engine_temp_c)
            VALUES (?, ?, ?, ?, ?)
        """, (r["vehicle_id"], r["timestamp"], r["speed_kmh"], r["battery_pct"], r["engine_temp_c"]))

    # Upsert aggregated summaries
    for s in summaries:
        cursor.execute("""
            INSERT OR REPLACE INTO vehicle_summary (vehicle_id, avg_speed, max_speed, avg_engine_temp, min_battery, readings_count)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (s["vehicle_id"], s["avg_speed"], s["max_speed"], s["avg_engine_temp"], s["min_battery"], s["readings_count"]))

    conn.commit()
    conn.close()
    print(f"[LOAD] Successfully loaded structured data into '{db_name}'.")