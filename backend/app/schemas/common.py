"""
CareerOS — Pydantic Schemas: Common types
"""
import uuid
from datetime import datetime

from pydantic import BaseModel


class ErrorResponse(BaseModel):
    error: str
    message: str
    request_id: str | None = None


class MessageResponse(BaseModel):
    message: str


class HealthStatus(BaseModel):
    status: str          # "ok" | "degraded" | "unavailable"
    detail: str | None = None
    latency_ms: float | None = None


class HealthResponse(BaseModel):
    status: str
    version: str = "1.0.0"
    env: str
    services: dict[str, HealthStatus] | None = None
