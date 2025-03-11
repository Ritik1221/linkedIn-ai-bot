#!/usr/bin/env python
"""
Script to optimize the database for the LinkedIn AI Agent.
"""

import logging
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.app.db.indexes import optimize_database
from src.app.core.logging import setup_logging

# Set up logging
setup_logging()
logger = logging.getLogger(__name__)

if __name__ == "__main__":
    logger.info("Starting database optimization")
    optimize_database()
    logger.info("Database optimization completed") 