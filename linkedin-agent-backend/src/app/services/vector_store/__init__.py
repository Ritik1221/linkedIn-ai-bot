"""
Vector store service module.
This module provides services for semantic search and job matching.
"""

from src.app.services.vector_store.client import VectorStoreService, get_vector_store_service

__all__ = ["VectorStoreService", "get_vector_store_service"] 