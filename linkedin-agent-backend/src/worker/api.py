"""
API module for Celery worker health checks and metrics.
This provides simple endpoints for monitoring the worker status.
"""

import logging
import json
from datetime import datetime
from typing import Dict, Any, List, Optional

from flask import Flask, jsonify, request
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST
import celery.states as states

from src.worker.main import celery_app
from src.worker.monitoring import create_task_report, APP_METRICS

logger = logging.getLogger(__name__)

app = Flask(__name__)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# Health check endpoint
@app.route('/health', methods=['GET'])
def health_check() -> Dict[str, Any]:
    """
    Health check endpoint for the worker.
    
    Returns:
        Dict containing health status
    """
    try:
        # Get celery stats
        stats = celery_app.control.inspect().stats()
        
        if not stats:
            return jsonify({
                "status": "error",
                "message": "No Celery workers found"
            }), 503
        
        # Get worker statuses
        worker_status = []
        for worker_name, worker_stats in stats.items():
            worker_status.append({
                "name": worker_name,
                "status": "online",
                "processed": worker_stats.get('total', {}).get('processed', 0),
                "active": len(celery_app.control.inspect().active().get(worker_name, [])),
                "scheduled": len(celery_app.control.inspect().scheduled().get(worker_name, [])),
                "reserved": len(celery_app.control.inspect().reserved().get(worker_name, []))
            })
        
        return jsonify({
            "status": "healthy",
            "workers": worker_status,
            "timestamp": datetime.utcnow().isoformat()
        })
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

# Metrics endpoint for Prometheus
@app.route('/metrics', methods=['GET'])
def metrics() -> str:
    """
    Prometheus metrics endpoint.
    
    Returns:
        Prometheus metrics in text format
    """
    return generate_latest(), 200, {'Content-Type': CONTENT_TYPE_LATEST}

# Task status endpoint
@app.route('/task/<task_id>', methods=['GET'])
def task_status(task_id: str) -> Dict[str, Any]:
    """
    Get the status of a specific task.
    
    Args:
        task_id: ID of the task to check
        
    Returns:
        Dict containing task status
    """
    task = celery_app.AsyncResult(task_id)
    
    response = {
        "task_id": task_id,
        "status": task.state,
        "timestamp": datetime.utcnow().isoformat()
    }
    
    if task.state == states.SUCCESS:
        response["result"] = task.result
    elif task.state == states.FAILURE:
        response["error"] = str(task.result)
    
    return jsonify(response)

# Task report endpoint
@app.route('/report', methods=['GET'])
def task_report() -> Dict[str, Any]:
    """
    Generate a report of task executions.
    
    Returns:
        Dict containing task execution statistics
    """
    days = request.args.get('days', default=7, type=int)
    
    try:
        report = create_task_report()
        
        # Add additional report info
        active_tasks = celery_app.control.inspect().active()
        report["active_tasks"] = sum(len(tasks) for tasks in active_tasks.values()) if active_tasks else 0
        
        scheduled_tasks = celery_app.control.inspect().scheduled()
        report["scheduled_tasks"] = sum(len(tasks) for tasks in scheduled_tasks.values()) if scheduled_tasks else 0
        
        return jsonify(report)
    except Exception as e:
        logger.error(f"Error generating task report: {str(e)}")
        return jsonify({
            "status": "error",
            "message": f"Error generating task report: {str(e)}"
        }), 500

# Custom metrics report
@app.route('/custom-metrics', methods=['GET'])
def custom_metrics() -> Dict[str, Any]:
    """
    Get a report of custom application metrics.
    
    Returns:
        Dict containing custom metrics
    """
    # This is a placeholder - in a real implementation, this would
    # fetch actual metrics from Prometheus or another storage system
    metrics_report = {
        "user_metrics": {
            "active_users": 0,  # Would be populated from metrics
            "users_with_linkedin": 0
        },
        "job_metrics": {
            "jobs_found_today": 0,
            "jobs_matched_today": 0
        },
        "application_metrics": {
            "applications_submitted_today": 0,
            "resumes_generated_today": 0,
            "cover_letters_generated_today": 0
        },
        "performance_metrics": {
            "avg_job_search_time": 0.0,
            "avg_profile_sync_time": 0.0,
            "avg_llm_response_time": 0.0
        },
        "timestamp": datetime.utcnow().isoformat()
    }
    
    return jsonify(metrics_report)

# Run the Flask app if this file is executed directly
if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=8001) 