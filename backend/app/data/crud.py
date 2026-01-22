from typing import List, Optional
from sqlalchemy.orm import Session

from app.data.models import Event


def create_event(
    db: Session,
    user_id: str,
    event_type: str,
    timestamp: str,
    source_ip: Optional[str] = None,
    resource: Optional[str] = None,
    success: Optional[bool] = None,
) -> Event:
    event = Event(
        user_id=user_id,
        event_type=event_type,
        source_ip=source_ip,
        resource=resource,
        success=success,
        timestamp=timestamp,
    )
    db.add(event)
    db.commit()
    db.refresh(event)
    return event


def list_events(db: Session, limit: int = 50) -> List[Event]:
    return (
        db.query(Event)
        .order_by(Event.id.desc())
        .limit(limit)
        .all()
    )


def list_all_events(db: Session) -> List[Event]:
    return (
        db.query(Event)
        .order_by(Event.id.asc())
        .all()
    )
