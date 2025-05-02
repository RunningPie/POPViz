from sqlalchemy.orm import Session
from .models import PredictionHistory

def add_prediction(db: Session, sequence: str, predicted_structure: str):
    new_entry = PredictionHistory(
        sequence=sequence,
        predicted_structure=predicted_structure
    )
    db.add(new_entry)
    db.commit()
    db.refresh(new_entry)
    return new_entry

def get_all_predictions(db: Session):
    return db.query(PredictionHistory).order_by(PredictionHistory.timestamp.desc()).all()
