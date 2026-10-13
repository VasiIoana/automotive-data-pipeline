import os
from pathlib import Path
from src.extract import extract_sensor_data
from src.transform import clean_telemetry_data, compute_vehicle_metrics
from src.load import load_data, get_database_connection


def run_pipeline():
    base_dir = Path(__file__).resolve().parent
    raw_file = str(base_dir / "data" / "raw_sensors.json")
    db_name = str(base_dir / "telemetry.db")

    print("=== AUTOMOTIVE DATA PIPELINE EXECUTION STARTED ===")

    # EXTRACT
    raw_data = extract_sensor_data(raw_file)

    # TRANSFORM
    clean_data = clean_telemetry_data(raw_data)
    summary_data = compute_vehicle_metrics(clean_data)

    # LOAD
    load_data(clean_data, summary_data, db_name)

    # VERIFY VIA SQL QUERY
    print("\n=== VERIFYING PERSISTED AGGREGATES (SQL QUERY) ===")
    conn = get_database_connection(db_name)
    cursor = conn.cursor()
    cursor.execute("SELECT vehicle_id, avg_speed, max_speed, min_battery, readings_count FROM vehicle_summary;")
    rows = cursor.fetchall()
    for row in rows:
        print(
            f"Vehicle: {row[0]:<8} | Avg Speed: {row[1]:>5} km/h | Max Speed: {row[2]:>5} km/h | Min Battery: {row[3]}% | Records: {row[4]}")
    conn.close()

    print("\n=== PIPELINE EXECUTION COMPLETED SUCCESSFULLY! ===")


if __name__ == "__main__":
    run_pipeline()