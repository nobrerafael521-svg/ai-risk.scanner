from sqlalchemy import Column, Integer, String, Boolean
from app.data.database import Base


class Event(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String(64), index=True, nullable=False)
    event_type = Column(String(64), nullable=False)
    source_ip = Column(String(64), nullable=True)
    resource = Column(String(256), nullable=True)
    success = Column(Boolean, nullable=True)
    timestamp = Column(String(64), nullable=False)
