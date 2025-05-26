from sqlalchemy import Column, Integer, String, DateTime
from .base import Base
from datetime import datetime

class PredictionHistory(Base):
    __tablename__ = "prediction_history"

    id = Column(Integer, primary_key=True, index=True)
    sequence = Column(String, nullable=False)
    predicted_structure = Column(String, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)
    synced = Column(Integer, default=0)  # 0 = not synced, 1 = synced
