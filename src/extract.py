import json
import os
from pathlib import Path
from typing import List, Dict, Any

SAMPLE_RECORDS = [
    {"vehicle_id": "CAR-001", "timestamp": "2026-10-13 10:00:00", "speed_kmh": 65.4, "battery_pct": 85, "engine_temp_c": 90.5},
    {"vehicle_id": "CAR-001", "timestamp": "2026-10-13 10:05:00", "speed_kmh": 72.1, "battery_pct": 84, "engine_temp_c": 92.0},
    {"vehicle_id": "CAR-001", "timestamp": "2026-10-13 10:10:00", "speed_kmh": -10.0, "battery_pct": 83, "engine_temp_c": 91.0},
    {"vehicle_id": "CAR-002", "timestamp": "2026-10-13 10:00:00", "speed_kmh": 110.5, "battery_pct": 45, "engine_temp_c": 95.0},
    {"vehicle_id": "CAR-002", "timestamp": "2026-10-13 10:05:00", "speed_kmh": 350.0, "battery_pct": 44, "engine_temp_c": 130.0},
    {"vehicle_id": "CAR-002", "timestamp": "2026-10-13 10:10:00", "speed_kmh": None, "battery_pct": 43, "engine_temp_c": 94.5},
    {"vehicle_id": "CAR-003", "timestamp": "2026-10-13 10:00:00", "speed_kmh": 50.0, "battery_pct": 98, "engine_temp_c": 88.0},
    {"vehicle_id": "CAR-003", "timestamp": "2026-10-13 10:05:00", "speed_kmh": 55.2, "battery_pct": 97, "engine_temp_c": 89.2}
]

def extract_sensor_data(file_path: str) -> List[Dict[str, Any]]:
    """
    Extracts raw telemetry sensor readings from a JSON source file.
    Creates sample dataset automatically if not present.
    """
    path_obj = Path(file_path)
    path_obj.parent.mkdir(parents=True, exist_ok=True)

    if not path_obj.exists():
        print(f"[EXTRACT] File not found. Automatically seeding sample data to: {file_path}")
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(SAMPLE_RECORDS, f, indent=2)

    with open(file_path, "r", encoding="utf-8") as f:
        raw_records = json.load(f)

    print(f"[EXTRACT] Ingested {len(raw_records)} raw records from {file_path}.")
    return raw_records