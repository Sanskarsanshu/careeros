"""
CareerOS — Application Configuration

All settings are read from environment variables.
Never hard-code secrets — use .env.example as reference.
"""
import logging
from functools import lru_cache
from typing import Literal

from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # ── App ──────────────────────────────────────────────────────────────────
    APP_ENV: Literal["development", "production", "test"] = "development"
    LOG_LEVEL: str = "INFO"

    # ── Database ─────────────────────────────────────────────────────────────
    DATABASE_URL: str = "postgresql+asyncpg://careeros:careeros@localhost:5432/careeros"
    DATABASE_SYNC_URL: str = "postgresql+psycopg2://careeros:careeros@localhost:5432/careeros"

    # ── Redis ────────────────────────────────────────────────────────────────
    REDIS_URL: str = "redis://localhost:6379/0"
    CELERY_BROKER_URL: str = "redis://localhost:6379/0"
    CELERY_RESULT_BACKEND: str = "redis://localhost:6379/1"

    # ── Auth ─────────────────────────────────────────────────────────────────
    AUTH_SECRET: str = "insecure-dev-secret-change-in-production"
    AUTH_ALGORITHM: str = "HS256"
    AUTH_ACCESS_TOKEN_EXPIRE_MINUTES: int = 15
    AUTH_REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    # ── CORS ─────────────────────────────────────────────────────────────────
    CORS_ORIGINS: str = "http://localhost:3000,http://127.0.0.1:3000"

    # ── Storage ──────────────────────────────────────────────────────────────
    STORAGE_BACKEND: Literal["local", "s3"] = "local"
    STORAGE_LOCAL_PATH: str = "./storage"
    MAX_UPLOAD_SIZE_BYTES: int = 10 * 1024 * 1024  # 10 MB
    S3_ENDPOINT: str = ""
    S3_BUCKET: str = ""
    S3_ACCESS_KEY: str = ""
    S3_SECRET_KEY: str = ""
    S3_REGION: str = "us-east-1"

    # ── LLM [Phase 4+] ───────────────────────────────────────────────────────
    LLM_PROVIDER: str = "openai"
    LLM_MODEL: str = "gpt-4o-mini"
    LLM_API_KEY: str = ""
    LLM_BASE_URL: str = ""

    # ── Embeddings [Phase 5+] ────────────────────────────────────────────────
    EMBEDDING_PROVIDER: str = "openai"
    EMBEDDING_MODEL: str = "text-embedding-3-small"
    EMBEDDING_DIMENSIONS: int = 1536
    EMBEDDING_API_KEY: str = ""

    # ── Reranker [Phase 5+] ──────────────────────────────────────────────────
    RERANKER_MODEL: str = "cross-encoder/ms-marco-MiniLM-L-6-v2"

    # ── RAG [Phase 5+] ───────────────────────────────────────────────────────
    RAG_CHUNK_SIZE: int = 800
    RAG_CHUNK_OVERLAP: int = 150
    RAG_TOP_K_RETRIEVAL: int = 20
    RAG_TOP_K_RERANKED: int = 5
    RAG_HYBRID_ALPHA: float = 0.6
    RAG_FAITHFULNESS_THRESHOLD: float = 0.7
    RAG_EMBEDDING_QUERY_CACHE_SIZE: int = 256

    # ── ATS Weights [Phase 4+] ───────────────────────────────────────────────
    ATS_WEIGHT_KEYWORD: float = 0.25
    ATS_WEIGHT_SKILL: float = 0.25
    ATS_WEIGHT_EXPERIENCE: float = 0.20
    ATS_WEIGHT_PROJECT: float = 0.10
    ATS_WEIGHT_EDUCATION: float = 0.10
    ATS_WEIGHT_STRUCTURE: float = 0.05
    ATS_WEIGHT_FORMATTING: float = 0.05

    @property
    def cors_origins_list(self) -> list[str]:
        return [o.strip() for o in self.CORS_ORIGINS.split(",") if o.strip()]

    @property
    def is_production(self) -> bool:
        return self.APP_ENV == "production"

    def configure_logging(self) -> None:
        """Set up structured JSON logging."""
        import sys
        from pythonjsonlogger.json import JsonFormatter

        handler = logging.StreamHandler(sys.stdout)
        handler.setFormatter(
            JsonFormatter(
                fmt="%(asctime)s %(levelname)s %(name)s %(message)s",
                datefmt="%Y-%m-%dT%H:%M:%S",
            )
        )
        root = logging.getLogger()
        root.setLevel(getattr(logging, self.LOG_LEVEL.upper(), logging.INFO))
        root.handlers.clear()
        root.addHandler(handler)


@lru_cache
def get_settings() -> Settings:
    s = Settings()
    s.configure_logging()
    return s


settings: Settings = get_settings()
