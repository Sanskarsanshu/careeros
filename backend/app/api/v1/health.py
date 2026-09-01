"""
CareerOS — Health Check API Routes
"""
import time
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
import redis.asyncio as aioredis

from app.core.config import settings
from app.core.dependencies import get_db, get_redis
from app.schemas.common import HealthResponse, HealthStatus

router = APIRouter(prefix="/health", tags=["health"])


@router.get("", response_model=HealthResponse)
async def health_check():
    """Basic health check to verify API is running."""
    return HealthResponse(
        status="ok",
        env=settings.APP_ENV
    )


@router.get("/db", response_model=HealthResponse)
async def db_health_check(db: AsyncSession = Depends(get_db)):
    """Health check that verifies PostgreSQL connection."""
    start = time.perf_counter()
    try:
        # Simple query to verify DB is responsive
        await db.execute(text("SELECT 1"))
        latency_ms = (time.perf_counter() - start) * 1000
        
        return HealthResponse(
            status="ok",
            env=settings.APP_ENV,
            services={
                "database": HealthStatus(status="ok", latency_ms=latency_ms)
            }
        )
    except Exception as e:
        latency_ms = (time.perf_counter() - start) * 1000
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail={
                "status": "unavailable",
                "env": settings.APP_ENV,
                "services": {
                    "database": HealthStatus(status="unavailable", detail=str(e), latency_ms=latency_ms).model_dump()
                }
            }
        )


@router.get("/redis", response_model=HealthResponse)
async def redis_health_check(redis: aioredis.Redis = Depends(get_redis)):
    """Health check that verifies Redis connection."""
    start = time.perf_counter()
    try:
        await redis.ping()
        latency_ms = (time.perf_counter() - start) * 1000
        
        return HealthResponse(
            status="ok",
            env=settings.APP_ENV,
            services={
                "redis": HealthStatus(status="ok", latency_ms=latency_ms)
            }
        )
    except Exception as e:
        latency_ms = (time.perf_counter() - start) * 1000
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail={
                "status": "unavailable",
                "env": settings.APP_ENV,
                "services": {
                    "redis": HealthStatus(status="unavailable", detail=str(e), latency_ms=latency_ms).model_dump()
                }
            }
        )
