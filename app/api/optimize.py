from fastapi import APIRouter, Depends, HTTPException
import numpy as np
from app.schemas import OptimizeRequest, OptimizeResult
from app.core.demand import predict, fit_linear
from app.models import ABObservation
from app.database import get_db
from sqlalchemy.orm import Session

router = APIRouter()

@router.post("", response_model=OptimizeResult)
def optimize(req: OptimizeRequest, db: Session = Depends(get_db)):
    rows = db.query(ABObservation).all()
    if len(rows) < 3:
        raise HTTPException(400, "Need more data")

    prices = np.array([r.price for r in rows])
    quantities = np.array([r.quantity for r in rows])
    fit = fit_linear(prices, quantities)
    model = {"type": "linear", "intercept": fit["intercept"],
             "slope": fit["slope"]}

    p_grid = np.linspace(max(1.0, prices.min()*0.3), prices.max()*2, 200)
    curve = []
    best = None
    for p in p_grid:
        q = predict(model, float(p))
        if req.objective == "revenue":
            value = float(p) * q
        else:
            value = (float(p) - req.unit_cost) * q
        curve.append({"price": float(p), "quantity": q, "value": value})
        if best is None or value > best["value"]:
            best = {"price": float(p), "quantity": q, "value": value}

    if best is None:
        raise HTTPException(500, "Optimization failed")

    return OptimizeResult(
        optimal_price=best["price"],
        optimal_quantity=best["quantity"],
        optimal_value=best["value"],
        curve=curve)
