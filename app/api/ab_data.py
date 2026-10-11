from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models import ABObservation
from app.schemas import ObservationCreate, ObservationRead

router = APIRouter()

@router.post("", response_model=ObservationRead, status_code=201)
def add(payload: ObservationCreate, db: Session = Depends(get_db)):
    o = ABObservation(**payload.model_dump())
    db.add(o)
    db.commit()
    db.refresh(o)
    return o

@router.get("", response_model=List[ObservationRead])
def list_all(experiment_id: str = None, db: Session = Depends(get_db)):
    q = db.query(ABObservation)
    if experiment_id:
        q = q.filter(ABObservation.experiment_id == experiment_id)
    return q.all()

@router.delete("/{obs_id}", status_code=204)
def delete(obs_id: int, db: Session = Depends(get_db)):
    o = db.query(ABObservation).get(obs_id)
    if o:
        db.delete(o)
        db.commit()
