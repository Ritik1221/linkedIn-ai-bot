#!/usr/bin/env python3
"""
Task scheduler for the LinkedIn AI Agent backend.
This script sets up periodic tasks using Celery Beat.
"""

import os
import sys
from pathlib import Path

# Add the parent directory to the path so we can import the app
sys.path.append(str(Path(__file__).parent.parent))

from celery import Celery
from celery.schedules import crontab

from src.app.core.config import settings

# Create Celery app
celery_app = Celery(
    "linkedin_agent_scheduler",
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
)

# Define scheduled tasks
celery_app.conf.beat_schedule = {
    # LinkedIn profile sync - every day at 2 AM
    "sync-profiles-daily": {
        "task": "src.worker.tasks.admin.sync_all_profiles",
        "schedule": crontab(hour=2, minute=0),
        "args": (),
    },
    
    # LinkedIn job search - every 4 hours
    "search-jobs-regularly": {
        "task": "src.worker.tasks.admin.search_jobs_for_all_users",
        "schedule": crontab(hour="*/4", minute=15),
        "args": (),
    },
    
    # Update vector index - every day at 3 AM
    "update-vector-index-daily": {
        "task": "src.worker.tasks.linkedin.bulk_index_jobs",
        "schedule": crontab(hour=3, minute=0),
        "args": (),
    },
    
    # Update profile vector index - every day at 3:30 AM
    "update-profile-vector-index-daily": {
        "task": "src.worker.tasks.linkedin.bulk_index_profiles",
        "schedule": crontab(hour=3, minute=30),
        "args": (),
    },
    
    # Find matching jobs for users - every day at 4 AM
    "find-matching-jobs-daily": {
        "task": "src.worker.tasks.admin.find_matching_jobs_for_all_users",
        "schedule": crontab(hour=4, minute=0),
        "args": (),
    },
    
    # Clean up old data - every week on Sunday at 1 AM
    "cleanup-old-data-weekly": {
        "task": "src.worker.tasks.admin.cleanup_old_data",
        "schedule": crontab(hour=1, minute=0, day_of_week="sunday"),
        "args": (),
    },
}

if __name__ == "__main__":
    celery_app.start() 