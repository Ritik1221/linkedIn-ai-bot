"""
Logging utilities for the LinkedIn AI Agent.
This module provides structured logging functionality.
"""

import json
import logging
import sys
from datetime import datetime
from typing import Any, Dict, Optional

import structlog
from structlog.types import EventDict, Processor

from src.app.core.config import settings


def add_timestamp(_, __, event_dict: EventDict) -> EventDict:
    """
    Add ISO-format timestamp to the event dict.
    """
    event_dict["timestamp"] = datetime.utcnow().isoformat()
    return event_dict


def add_environment_info(_, __, event_dict: EventDict) -> EventDict:
    """
    Add environment information to the event dict.
    """
    event_dict["environment"] = settings.ENVIRONMENT
    event_dict["app_name"] = settings.PROJECT_NAME
    return event_dict


def setup_logging(
    log_level: str = "INFO",
    json_format: bool = True,
    console_output: bool = True,
    file_output: bool = False,
    log_file: Optional[str] = None,
) -> None:
    """
    Setup structured logging.
    
    Args:
        log_level: Log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        json_format: Whether to use JSON format for logs
        console_output: Whether to output logs to console
        file_output: Whether to output logs to file
        log_file: Log file path (if file_output is True)
    """
    log_level_num = getattr(logging, log_level.upper(), logging.INFO)
    
    # Configure processors based on format
    processors = [
        structlog.stdlib.filter_by_level,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.UnicodeDecoder(),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        add_timestamp,
        add_environment_info,
    ]
    
    if json_format:
        processors.append(structlog.processors.JSONRenderer())
    else:
        processors.append(structlog.dev.ConsoleRenderer())
    
    # Configure structlog
    structlog.configure(
        processors=processors,
        context_class=dict,
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=True,
    )
    
    # Setup handlers
    handlers = []
    
    if console_output:
        console_handler = logging.StreamHandler(sys.stdout)
        handlers.append(console_handler)
    
    if file_output and log_file:
        file_handler = logging.FileHandler(log_file)
        handlers.append(file_handler)
    
    # Configure standard logging
    logging.basicConfig(
        format="%(message)s",
        level=log_level_num,
        handlers=handlers,
    )


def get_logger(name: str) -> structlog.stdlib.BoundLogger:
    """
    Get structured logger.
    
    Args:
        name: Logger name
        
    Returns:
        Structured logger
    """
    return structlog.get_logger(name)


# Helper function to log API request details
def log_api_request(
    logger: structlog.stdlib.BoundLogger,
    request_id: str,
    method: str,
    endpoint: str,
    user_id: Optional[str] = None,
    extra: Optional[Dict[str, Any]] = None,
) -> None:
    """
    Log API request details.
    
    Args:
        logger: Structured logger
        request_id: Request ID
        method: HTTP method
        endpoint: API endpoint
        user_id: User ID (if authenticated)
        extra: Additional information to log
    """
    log_data = {
        "request_id": request_id,
        "method": method,
        "endpoint": endpoint,
    }
    
    if user_id:
        log_data["user_id"] = user_id
        
    if extra:
        log_data.update(extra)
        
    logger.info("api_request", **log_data)


# Helper function to log API response details
def log_api_response(
    logger: structlog.stdlib.BoundLogger,
    request_id: str,
    status_code: int,
    duration_ms: float,
    extra: Optional[Dict[str, Any]] = None,
) -> None:
    """
    Log API response details.
    
    Args:
        logger: Structured logger
        request_id: Request ID
        status_code: HTTP status code
        duration_ms: Request duration in milliseconds
        extra: Additional information to log
    """
    log_data = {
        "request_id": request_id,
        "status_code": status_code,
        "duration_ms": duration_ms,
    }
        
    if extra:
        log_data.update(extra)
        
    logger.info("api_response", **log_data) 