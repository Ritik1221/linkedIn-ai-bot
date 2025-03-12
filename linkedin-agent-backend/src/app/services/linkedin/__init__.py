"""
LinkedIn API service module.
This module provides services for interacting with the LinkedIn API.
"""

from src.app.services.linkedin.client import LinkedInService, get_linkedin_service

__all__ = ["LinkedInService", "get_linkedin_service"] 