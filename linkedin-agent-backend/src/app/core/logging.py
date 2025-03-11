"""
Logging configuration for the LinkedIn AI Agent.
"""

import logging
import sys
from typing import Dict, Any

from src.app.core.config import settings

# Log format
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

# Log level mapping
LOG_LEVEL_MAP = {
    "DEBUG": logging.DEBUG,
    "INFO": logging.INFO,
    "WARNING": logging.WARNING,
    "ERROR": logging.ERROR,
    "CRITICAL": logging.CRITICAL,
}

def setup_logging() -> None:
    """
    Set up logging for the application.
    """
    log_level = LOG_LEVEL_MAP.get(settings.LOG_LEVEL, logging.INFO)
    
    # Configure root logger
    logging.basicConfig(
        level=log_level,
        format=LOG_FORMAT,
        handlers=[
            logging.StreamHandler(sys.stdout),
            logging.FileHandler("logs/app.log", mode="a"),
        ],
    )
    
    # Set log levels for specific loggers
    logging.getLogger("uvicorn").setLevel(log_level)
    logging.getLogger("uvicorn.access").setLevel(log_level)
    logging.getLogger("sqlalchemy.engine").setLevel(logging.WARNING)
    
    # Log startup message
    logging.info(f"Logging configured with level: {settings.LOG_LEVEL}")

def get_logger(name: str) -> logging.Logger:
    """
    Get a logger with the specified name.
    
    Args:
        name: The name of the logger
        
    Returns:
        The logger instance
    """
    return logging.getLogger(name) 