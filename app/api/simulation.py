from fastapi import APIRouter, Depends, HTTPException
import numpy as np
from app.schemas import ABTestRequest, ABTestResult
from app.core.ab_test import ab_test as run_ab
from app.core.segments import segment_optimal, DEFAULT_SEGMENTS
from app.models import ABObservation
from app.database import get_db
from sqlalchemy.orm import Session

router = APIRouter()

@router.post("/ab", response_model=ABTestResult)
def ab(req: ABTestRequest, db: Session = Depends(get_db)):
    a = db.query(ABObservation).filter(
        ABObservation.price.between(req.price_a - 1, req.price_a + 1)).all()
    b = db.query(ABObservation).filter(
        ABObservation.price.between(req.price_b - 1, req.price_b + 1)).all()
    if len(a) < 2 or len(b) < 2:
        raise HTTPException(400, "Not enough data for both prices")
    result = run_ab([x.quantity for x in a], [x.quantity for x in b],
                    req.price_a, req.price_b)
    return ABTestResult(**result)

@router.get("/segments")
def segments():
    return segment_optimal(DEFAULT_SEGMENTS)

@router.post("/competitor")
def competitor(our_price: float, comp_price: float, cross_elasticity: float = 0.5):
    intercept = 1000.0
    slope = -4.0
    base_q = max(0.0, intercept + slope * our_price)
    adjusted = max(0.0, base_q * (1 - cross_elasticity * (comp_price - our_price) / our_price))
    return {"our_price": our_price, "competitor_price": comp_price,
            "expected_quantity": round(adjusted, 2)}
