from pydantic_settings import BaseSettings
from typing import Optional
import os


class Settings(BaseSettings):
    app_name: str = "Insurance Copilot"
    app_version: str = "1.0.0"
    debug: bool = False

    database_url: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/insurance_copilot"
    database_url_sync: str = "postgresql+psycopg2://postgres:postgres@localhost:5432/insurance_copilot"

    clerk_api_key: str = ""
    clerk_jwt_pub_key: str = ""
    clerk_webhook_secret: str = ""

    groq_api_key: str = ""
    groq_model: str = "llama3-70b-8192"

    tavily_api_key: Optional[str] = None

    upload_dir: str = "uploads"
    max_upload_size_mb: int = 50
    allowed_extensions: list[str] = [".pdf", ".png", ".jpg", ".jpeg", ".tiff"]

    pgvector_dimension: int = 384
    chunk_size: int = 512
    chunk_overlap: int = 64
    top_k_retrieval: int = 5

    redis_url: str = "redis://localhost:6379/0"
    celery_broker_url: str = "redis://localhost:6379/1"

    storage_backend: str = "local"
    s3_endpoint: Optional[str] = None
    s3_access_key: Optional[str] = None
    s3_secret_key: Optional[str] = None
    s3_bucket: Optional[str] = None

    cors_origins: list[str] = ["http://localhost:5173", "http://localhost:3000"]

    log_level: str = "INFO"
    sentry_dsn: Optional[str] = None

    rate_limit_per_minute: int = 60
    rate_limit_per_hour: int = 1000

    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()
