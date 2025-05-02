import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .base import Base
from .models import PredictionHistory

DB_PATH = os.path.join(os.getcwd(), "db.sqlite3")
engine = create_engine(f"sqlite:///{DB_PATH}", connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

def init_db():
    Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
