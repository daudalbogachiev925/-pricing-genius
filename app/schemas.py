from typing import List, Optional
from pydantic import BaseModel, Field

class ObservationCreate(BaseModel):
    experiment_id: str
    price: float = Field(gt=0)
    quantity: int = Field(ge=0)
    segment: str = "default"

class ObservationRead(ObservationCreate):
    id: int

    class Config:
        from_attributes = True

class DemandFitRequest(BaseModel):
    experiment_id: Optional[str] = None
    model_type: str = "linear"

class DemandFitResult(BaseModel):
    model_type: str
    params: dict
    r_squared: float
    aic: float
    n_samples: int

class ElasticityPoint(BaseModel):
    price: float
    elasticity: float

class ElasticityResponse(BaseModel):
    current_price: float
    current_elasticity: float
    points: List[ElasticityPoint]

class OptimizeRequest(BaseModel):
    model_type: str = "linear"
    unit_cost: float = 30.0
    objective: str = "profit"  # profit / revenue

class OptimizeResult(BaseModel):
    optimal_price: float
    optimal_quantity: float
    optimal_value: float
    curve: List[dict]

class ABTestRequest(BaseModel):
    price_a: float
    price_b: float

class ABTestResult(BaseModel):
    revenue_a: float
    revenue_b: float
    t_stat: float
    p_value: float
    significant: bool
    winner: str
