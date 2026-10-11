from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import Base, engine
from app.api import ab_data, models, optimize, simulation

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Pricing Genius", version="1.0.0")
app.add_middleware(CORSMiddleware, allow_origins=["*"],
                   allow_methods=["*"], allow_headers=["*"])

app.include_router(ab_data.router, prefix="/api/ab-data", tags=["ab-data"])
app.include_router(models.router, prefix="/api/models", tags=["models"])
app.include_router(optimize.router, prefix="/api/optimize", tags=["optimize"])
app.include_router(simulation.router, prefix="/api/simulation", tags=["simulation"])

@app.get("/health")
def health():
    return {"status": "ok"}
