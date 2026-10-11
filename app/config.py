from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql://user:pass@db:5432/pricing"
    UNIT_COST: float = 30.0
    MIN_PRICE: float = 10.0
    MAX_PRICE: float = 500.0
    PRICE_STEP: int = 200

    class Config:
        env_file = ".env"

settings = Settings()
