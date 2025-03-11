"""
Task package for the LinkedIn AI Agent.
"""

# Import tasks to register them with Celery
from src.worker.tasks import linkedin_tasks, llm_tasks 