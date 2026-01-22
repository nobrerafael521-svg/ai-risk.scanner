from typing import List, Dict
from datetime import datetime, timedelta




def detect_burst_activity(
    events: List[Dict],
    window_minutes: int = 5,
    threshold: int = 10
) -> List[Dict]:
    """
    Detects abnormal burst activity:
    - Too many events from the same user in a short time window
    """
    suspicious = []
    events_sorted = sorted(events, key=lambda e: e.get("timestamp", ""))

    for i, e in enumerate(events_sorted):
        user_id = e.get("user_id")
        ts_raw = e.get("timestamp")

        try:
            ts = datetime.fromisoformat(ts_raw.replace("Z", ""))
        except Exception:
            continue

        count = 1
        for j in range(i + 1, len(events_sorted)):
            next_e = events_sorted[j]
            if next_e.get("user_id") != user_id:
                continue

            try:
                next_ts = datetime.fromisoformat(next_e.get("timestamp").replace("Z", ""))
            except Exception:
                continue

            if next_ts - ts <= timedelta(minutes=window_minutes):
                count += 1
            else:
                break

        if count >= threshold:
            suspicious.append({
                "user_id": user_id,
                "timestamp": ts_raw,
                "event_count": count,
                "type": "burst_activity"
            })

    return suspicious
