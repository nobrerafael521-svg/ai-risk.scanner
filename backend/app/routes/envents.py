from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

from sqlalchemy.orm import Session

from app.data.database import get_db
from app.data import crud

router = APIRouter()


class EventIn(BaseModel):
    user_id: str = Field(..., min_length=1, max_length=64)
    event_type: str = Field(..., min_length=1, max_length=64)  
    source_ip: Optional[str] = Field(default=None, max_length=64)
    resource: Optional[str] = Field(default=None, max_length=256)
    success: Optional[bool] = None
    timestamp: Optional[str] = None  


class EventOut(BaseModel):
    id: int
    user_id: str
    event_type: str
    source_ip: Optional[str]
    resource: Optional[str]
    success: Optional[bool]
    timestamp: str


def _to_event_out(e) -> dict:
    return {
        "id": e.id,
        "user_id": e.user_id,
        "event_type": e.event_type,
        "source_ip": e.source_ip,
        "resource": e.resource,
        "success": e.success,
        "timestamp": e.timestamp,
    }


@router.post("", response_model=EventOut)
def ingest_event(payload: EventIn, db: Session = Depends(get_db)):
    ts = payload.timestamp or datetime.utcnow().isoformat()

    created = crud.create_event(
        db=db,
        user_id=payload.user_id.strip(),
        event_type=payload.event_type.strip(),
        timestamp=ts,
        source_ip=payload.source_ip.strip() if payload.source_ip else None,
        resource=payload.resource.strip() if payload.resource else None,
        success=payload.success,
    )

    return _to_event_out(created)


@router.get("", response_model=List[EventOut])
def list_events(limit: int = 50, db: Session = Depends(get_db)):
    if limit < 1 or limit > 500:
        raise HTTPException(status_code=400, detail="limit must be between 1 and 500")

    items = crud.list_events(db=db, limit=limit)
 
 
    return [_to_event_out(e) for e in items]
