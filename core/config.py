import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "Lead Generation SaaS"
    # Security
    SECRET_KEY: str = os.environ.get("SECRET_KEY", "supersecretkey_please_change_in_production")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    
    # Database
    DATABASE_URL: str = os.environ.get("DATABASE_URL", "postgresql://postgres:127081@localhost:5432/project")
    
    class Config:
        env_file = ".env"

settings = Settings()
