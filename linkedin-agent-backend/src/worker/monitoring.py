"""
Monitoring module for the LinkedIn AI Agent.

This module provides utilities for tracking system performance,
celery task execution, and application statistics.
"""

import logging
import time
from functools import wraps
from typing import Dict, Any, List, Callable, Optional
from datetime import datetime

from prometheus_client import Counter, Histogram, Gauge, Summary
from celery.signals import task_success, task_failure, task_received, task_revoked

logger = logging.getLogger(__name__)

# Initialize metrics
TASK_COUNTER = Counter(
    'celery_tasks_total', 
    'Number of celery tasks', 
    ['task_name', 'state']
)

TASK_LATENCY = Histogram(
    'celery_task_latency_seconds', 
    'Task execution time in seconds', 
    ['task_name']
)

APP_METRICS = {
    'profiles_synced': Counter(
        'profiles_synced_total', 
        'Number of LinkedIn profiles synced'
    ),
    'jobs_found': Counter(
        'jobs_found_total', 
        'Number of jobs found'
    ),
    'applications_submitted': Counter(
        'applications_submitted_total', 
        'Number of job applications submitted'
    ),
    'resumes_generated': Counter(
        'resumes_generated_total', 
        'Number of resumes generated'
    ),
    'cover_letters_generated': Counter(
        'cover_letters_generated_total', 
        'Number of cover letters generated'
    ),
    'job_search_duration': Histogram(
        'job_search_duration_seconds', 
        'Job search duration in seconds'
    ),
    'profile_sync_duration': Histogram(
        'profile_sync_duration_seconds', 
        'Profile sync duration in seconds'
    ),
    'llm_response_time': Histogram(
        'llm_response_time_seconds', 
        'LLM response time in seconds'
    ),
    'active_users': Gauge(
        'active_users', 
        'Number of active users'
    ),
    'pending_applications': Gauge(
        'pending_applications', 
        'Number of pending job applications'
    ),
    'error_rate': Counter(
        'error_rate_total', 
        'Number of errors by type',
        ['error_type', 'task_name']
    )
}

# Celery task signal handlers
@task_received.connect
def task_received_handler(sender=None, headers=None, body=None, **kwargs):
    task_name = sender.name if sender else 'unknown'
    TASK_COUNTER.labels(task_name=task_name, state='received').inc()

@task_success.connect
def task_success_handler(sender=None, **kwargs):
    task_name = sender.name if sender else 'unknown'
    TASK_COUNTER.labels(task_name=task_name, state='success').inc()

@task_failure.connect
def task_failure_handler(sender=None, exception=None, **kwargs):
    task_name = sender.name if sender else 'unknown'
    error_type = type(exception).__name__ if exception else 'unknown'
    TASK_COUNTER.labels(task_name=task_name, state='failure').inc()
    APP_METRICS['error_rate'].labels(error_type=error_type, task_name=task_name).inc()

@task_revoked.connect
def task_revoked_handler(sender=None, **kwargs):
    task_name = sender.name if sender else 'unknown'
    TASK_COUNTER.labels(task_name=task_name, state='revoked').inc()

def timing_decorator(metric_name: str) -> Callable:
    """
    Decorator for timing function execution.
    
    Args:
        metric_name: Name of the metric to use for timing
        
    Returns:
        Decorator function
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            start_time = time.time()
            try:
                result = func(*args, **kwargs)
                return result
            finally:
                execution_time = time.time() - start_time
                if metric_name in APP_METRICS:
                    APP_METRICS[metric_name].observe(execution_time)
                else:
                    logger.warning(f"Unknown metric name: {metric_name}")
        return wrapper
    return decorator

# Context manager for timing code blocks
class TimingContext:
    """
    Context manager for timing code blocks.
    
    Example:
        with TimingContext('job_search_duration'):
            # Code to time
    """
    def __init__(self, metric_name: str):
        self.metric_name = metric_name
        self.start_time = None
        
    def __enter__(self):
        self.start_time = time.time()
        return self
        
    def __exit__(self, exc_type, exc_val, exc_tb):
        execution_time = time.time() - self.start_time
        if self.metric_name in APP_METRICS:
            APP_METRICS[self.metric_name].observe(execution_time)
        else:
            logger.warning(f"Unknown metric name: {self.metric_name}")

def track_event(metric_name: str, increment: float = 1.0) -> None:
    """
    Track an application event.
    
    Args:
        metric_name: Name of the metric to increment
        increment: Value to increment by (default: 1.0)
    """
    if metric_name in APP_METRICS:
        if hasattr(APP_METRICS[metric_name], 'inc'):
            APP_METRICS[metric_name].inc(increment)
        else:
            logger.warning(f"Metric {metric_name} does not support increment")
    else:
        logger.warning(f"Unknown metric name: {metric_name}")

def set_gauge(metric_name: str, value: float) -> None:
    """
    Set a gauge metric value.
    
    Args:
        metric_name: Name of the gauge metric
        value: Value to set
    """
    if metric_name in APP_METRICS:
        if hasattr(APP_METRICS[metric_name], 'set'):
            APP_METRICS[metric_name].set(value)
        else:
            logger.warning(f"Metric {metric_name} is not a gauge")
    else:
        logger.warning(f"Unknown metric name: {metric_name}")

def create_task_report() -> Dict[str, Any]:
    """
    Create a report of task executions.
    
    Returns:
        Dictionary containing task execution statistics
    """
    # This is a placeholder - in a real implementation, this would
    # query Prometheus or another metrics storage system
    return {
        "timestamp": datetime.utcnow().isoformat(),
        "metrics": {
            "task_count": {
                "total": 0,  # Would be populated from metrics data
                "success": 0,
                "failure": 0,
                "pending": 0
            },
            "latency": {
                "avg": 0.0,  # Would be populated from metrics data
                "p95": 0.0,
                "p99": 0.0
            },
            "error_rate": 0.0  # Would be populated from metrics data
        }
    }

def track_application_progress(user_id: str, job_id: str, stage: str) -> None:
    """
    Track application progress through various stages.
    
    Args:
        user_id: ID of the user
        job_id: ID of the job
        stage: Stage of the application process
    """
    logger.info(f"Application progress: User {user_id}, Job {job_id}, Stage: {stage}")
    # In a real implementation, this might store progress in a database
    # or increment a custom metric with labels
    
    if stage == "resume_generated":
        track_event("resumes_generated")
    elif stage == "cover_letter_generated":
        track_event("cover_letters_generated")
    elif stage == "application_submitted":
        track_event("applications_submitted")

def export_metrics_to_file(path: str) -> None:
    """
    Export current metrics to a file.
    
    Args:
        path: File path to export metrics to
    """
    # This is a placeholder - in a real implementation, this would
    # export metrics from Prometheus or another metrics system
    logger.info(f"Exporting metrics to file: {path}") 