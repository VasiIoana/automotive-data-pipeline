from typing import List, Dict, Any


def clean_telemetry_data(raw_data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Cleans telemetry data by filtering missing fields and out-of-bounds sensor anomalies.
    """
    clean_records = []

    for row in raw_data:
        speed = row.get("speed_kmh")
        battery = row.get("battery_pct")
        vehicle_id = row.get("vehicle_id")
        timestamp = row.get("timestamp")
        temp = row.get("engine_temp_c")

        # Skip records with missing critical fields
        if speed is None or battery is None or not vehicle_id or not timestamp:
            continue

        # Filter domain-specific sensor outliers:
        # -Speed cannot be negative or exceed physical vehicle boundaries (0-250 km/h)
        # -Battery level must be valid percentage (0-100%)
        if not (0 <= speed <= 250):
            continue
        if not (0 <= battery <= 100):
            continue

        clean_records.append({
            "vehicle_id": vehicle_id,
            "timestamp": timestamp,
            "speed_kmh": float(speed),
            "battery_pct": int(battery),
            "engine_temp_c": float(temp) if temp is not None else 0.0
        })

    dropped_count = len(raw_data) - len(clean_records)
    print(
        f"[TRANSFORM] Data cleansing complete: dropped {dropped_count} invalid records. Retained: {len(clean_records)}.")
    return clean_records


def compute_vehicle_metrics(clean_records: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Computes aggregated performance metrics grouped by vehicle ID.
    """
    grouped = {}
    for row in clean_records:
        v_id = row["vehicle_id"]
        if v_id not in grouped:
            grouped[v_id] = {
                "speeds": [],
                "temps": [],
                "batteries": []
            }
        grouped[v_id]["speeds"].append(row["speed_kmh"])
        grouped[v_id]["temps"].append(row["engine_temp_c"])
        grouped[v_id]["batteries"].append(row["battery_pct"])

    summary = []
    for v_id, stats in grouped.items():
        avg_speed = round(sum(stats["speeds"]) / len(stats["speeds"]), 2)
        max_speed = round(max(stats["speeds"]), 2)
        avg_temp = round(sum(stats["temps"]) / len(stats["temps"]), 2)
        min_battery = min(stats["batteries"])
        count = len(stats["speeds"])

        summary.append({
            "vehicle_id": v_id,
            "avg_speed": avg_speed,
            "max_speed": max_speed,
            "avg_engine_temp": avg_temp,
            "min_battery": min_battery,
            "readings_count": count
        })

    print(f"[TRANSFORM] Aggregation complete for {len(summary)} unique vehicle(s).")
    return summary