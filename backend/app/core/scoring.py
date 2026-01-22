from typing import Dict, List, Tuple
from datetime import datetime

from app.core.detection import detect_burst_activity



RISK_WEIGHTS: Dict[str, int] = {
    "login_failed": 15,
    "login_success_off_hours": 10,
    "file_access_sensitive": 20,
    "many_events_short_time": 15,  
}


SENSITIVE_KEYWORDS = [
    "payroll", "hr", "finance", "secret", "confidential", "clients", "contracts"
]


def _is_off_hours(ts_iso: str) -> bool:
    """
    Off-hours definition (MVP):
    - weekdays: before 08:00 or after 19:00
    - weekend: always off-hours
    Uses UTC timestamps for now.
    """
    try:
        dt = datetime.fromisoformat(ts_iso.replace("Z", ""))
    except Exception:
        return False

    weekday = dt.weekday()  #
    hour = dt.hour

    if weekday >= 5: 
        return True

    return hour < 8 or hour >= 19


def _is_sensitive_resource(resource: str | None) -> bool:
    if not resource:
        return False
    r = resource.lower()
    return any(k in r for k in SENSITIVE_KEYWORDS)


def score_event(event: Dict, known_ips_by_user: Dict[str, set]) -> Tuple[int, List[str]]:
    """
    Scores a single event and returns:
    - points (int)
    - reasons (list of strings, explainable)
    """
    points = 0
    reasons: List[str] = []

    event_type = (event.get("event_type") or "").strip().lower()
    user_id = event.get("user_id")
    ts = event.get("timestamp") or ""
    source_ip = event.get("source_ip")
    resource = event.get("resource")
    success = event.get("success")

  
    if event_type == "login_failed":
        points += RISK_WEIGHTS["login_failed"]
        reasons.append("Failed login attempt")

    
    if event_type == "login" and success is True and _is_off_hours(ts):
        points += RISK_WEIGHTS["login_success_off_hours"]
        reasons.append("Successful login during off-hours")


    if event_type in {"file_access", "download"} and _is_sensitive_resource(resource):
        points += RISK_WEIGHTS["file_access_sensitive"]
        reasons.append("Access to a sensitive resource")

    if user_id and source_ip:
        known = known_ips_by_user.setdefault(user_id, set())
        if source_ip not in known:
          
            if len(known) >= 1:
                points += RISK_WEIGHTS["new_ip"]
                reasons.append("New IP address for this user")
            known.add(source_ip)

    return points, reasons


def apply_behavioral_detection(events: List[Dict], user_risk: Dict[str, Dict]) -> None:
    """
    Applies behavioral detections (burst activity) to the aggregated user risk.
    Mutates user_risk in place.
    """
    bursts = detect_burst_activity(events)

    for b in bursts:
        user_id = b.get("user_id") or "unknown"

        if user_id not in user_risk:
            user_risk[user_id] = {"score": 0, "high_risk_events": 0, "reasons": {}}

       
        user_risk[user_id]["score"] += 25
        user_risk[user_id]["high_risk_events"] += 1

        reason = "Abnormal burst activity detected"
        user_risk[user_id]["reasons"][reason] = (
            user_risk[user_id]["reasons"].get(reason, 0) + 1
        )


def aggregate_user_risk(events: List[Dict]) -> Dict[str, Dict]:
    """
    Aggregates risk per user from a list of events.
    Returns:
    {
      "user_id": {
        "score": int,
        "high_risk_events": int,
        "reasons": { reason: count }
      }
    }
    """
    known_ips_by_user: Dict[str, set] = {}
    result: Dict[str, Dict] = {}

    for e in events:
        user_id = e.get("user_id") or "unknown"

        pts, reasons = score_event(e, known_ips_by_user)

        if user_id not in result:
            result[user_id] = {"score": 0, "high_risk_events": 0, "reasons": {}}

        result[user_id]["score"] += pts

        if pts >= 20:
            result[user_id]["high_risk_events"] += 1

        for r in reasons:
            result[user_id]["reasons"][r] = result[user_id]["reasons"].get(r, 0) + 1

    
    apply_behavioral_detection(events, result)

    return result
