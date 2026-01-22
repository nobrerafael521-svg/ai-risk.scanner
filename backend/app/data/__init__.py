from app.data.database import Base, engine
from app.data import models

def init_db():
    Base.metadata.create_all(bind=engine)
