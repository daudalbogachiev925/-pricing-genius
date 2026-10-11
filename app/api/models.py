from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import json
import numpy as np
from app.database import get_db
from app.models import ABObservation, DemandModel
from app.schemas import DemandFitRequest, DemandFitResult
from app.core.demand import fit_linear, fit_log_log

router = APIRouter()

@router.post("/fit", response_model=DemandFitResult)
def fit(req: DemandFitRequest, db: Session = Depends(get_db)):
    q = db.query(ABObservation)
    if req.experiment_id:
        q = q.filter(ABObservation.experiment_id == req.experiment_id)
    rows = q.all()
    if len(rows) < 3:
        raise HTTPException(400, "Need at least 3 observations")

    prices = np.array([r.price for r in rows])
    quantities = np.array([r.quantity for r in rows])

    if req.model_type == "linear":
        result = fit_linear(prices, quantities)
        params = {"intercept": result["intercept"], "slope": result["slope"]}
    elif req.model_type == "log_log":
        result = fit_log_log(prices, quantities)
        params = {"a": result["a"], "b": result["b"]}
    else:
        raise HTTPException(400, "Unknown model type")

    name = f"{req.model_type}_{req.experiment_id or 'all'}"
    existing = db.query(DemandModel).filter(DemandModel.name == name).first()
    if existing:
        existing.params = json.dumps(params)
        existing.model_type = req.model_type
    else:
        db.add(DemandModel(name=name, model_type=req.model_type,
                           params=json.dumps(params)))
    db.commit()

    return DemandFitResult(
        model_type=req.model_type, params=params,
        r_squared=result["r_squared"], aic=result["aic"],
        n_samples=len(rows))

@router.get("/{name}")
def get_model(name: str, db: Session = Depends(get_db)):
    m = db.query(DemandModel).filter(DemandModel.name == name).first()
    if not m:
        raise HTTPException(404)
    return {"name": m.name, "model_type": m.model_type,
            "params": json.loads(m.params)}
