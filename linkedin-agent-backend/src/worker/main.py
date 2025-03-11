"""
Celery worker entry point for the LinkedIn AI Agent backend.
"""

import os
from celery import Celery

from src.app.core.config import settings

# Create Celery app
celery_app = Celery(
    "linkedin_agent",
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_RESULT_BACKEND,
)

# Configure Celery
celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    worker_prefetch_multiplier=1,
    task_acks_late=True,
    task_reject_on_worker_lost=True,
    task_track_started=True,
)

# Import tasks
celery_app.autodiscover_tasks(["src.worker.tasks"], force=True)

if __name__ == "__main__":
    celery_app.start() 