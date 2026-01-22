from fastapi import APIRouter, Depends
from typing import Dict, Any, List

from sqlalchemy.orm import Session

from app.data.database import get_db
from app.data import crud
from app.core.scoring import aggregate_user_risk

router = APIRouter()


def _event_to_dict(e) -> dict:
    return {
        "id": e.id,
        "user_id": e.user_id,
        "event_type": e.event_type,
        "source_ip": e.source_ip,
        "resource": e.resource,
        "success": e.success,
        "timestamp": e.timestamp,
    }


@router.get("/summary")
def risk_summary(db: Session = Depends(get_db)) -> Dict[str, Any]:
    events_db = crud.list_all_events(db=db)
    events = [_event_to_dict(e) for e in events_db]

    total_events = len(events)
    users_risk = aggregate_user_risk(events)

    total_users = len(users_risk)
    high_risk_users = sum(1 for u in users_risk.values() if u["score"] >= 50)

    top_user_id = None
    top_user_score = 0
    for uid, data in users_risk.items():
        if data["score"] > top_user_score:
            top_user_score = data["score"]
            top_user_id = uid

    return {
        "total_events": total_events,
        "total_users": total_users,
        "high_risk_users": high_risk_users,
        "top_user": {"user_id": top_user_id, "score": top_user_score} if top_user_id else None,
    }


@router.get("/users")
def risk_users(db: Session = Depends(get_db)) -> Dict[str, Any]:
    events_db = crud.list_all_events(db=db)
    events = [_event_to_dict(e) for e in events_db]

    users_risk = aggregate_user_risk(events)

    items = [
        {
            "user_id": uid,
            "score": data["score"],
            "high_risk_events": data["high_risk_events"],
            "reasons": data["reasons"],
        }
        for uid, data in users_risk.items()
    ]
    items.sort(key=lambda x: x["score"], reverse=True)

    return {"items": items}


@router.get("/events")
def suspicious_events(db: Session = Depends(get_db)) -> Dict[str, Any]:
    """
    Returns a simple suspicious feed (MVP):
    - login_failed
    - file_access/download to sensitive resources
    """
    events_db = crud.list_all_events(db=db)
    events = [_event_to_dict(e) for e in events_db]

    sensitive_keywords = ["payroll", "hr", "finance", "secret", "confidential", "clients", "contracts"]

    suspicious: List[dict] = []
    for e in events:
        event_type = (e.get("event_type") or "").lower()
        resource = (e.get("resource") or "").lower()

        if event_type == "login_failed":
            suspicious.append(e)
            continue

        if event_type in {"file_access", "download"} and any(k in resource for k in sensitive_keywords):
            suspicious.append(e)
            continue

    return {"items": suspicious[-100:]}
