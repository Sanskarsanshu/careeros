"""
CareerOS — Celery Health Tasks
"""
from app.workers.celery_app import celery_app

@celery_app.task(name="app.workers.health_tasks.health_check_task")
def health_check_task(message: str) -> dict:
    """A simple task to verify Celery is working."""
    return {"status": "ok", "message": f"Worker received: {message}"}
