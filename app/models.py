from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.sql import func
from app.database import Base

class ABObservation(Base):
    __tablename__ = "ab_observations"

    id = Column(Integer, primary_key=True)
    experiment_id = Column(String, index=True)
    price = Column(Float, nullable=False, index=True)
    quantity = Column(Integer, nullable=False)
    segment = Column(String, default="default")
    created_at = Column(DateTime, server_default=func.now())

class DemandModel(Base):
    __tablename__ = "demand_models"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    model_type = Column(String, nullable=False)  # linear / log_log
    params = Column(String, nullable=False)  # JSON
    unit_cost = Column(Float, default=30.0)
    created_at = Column(DateTime, server_default=func.now())
