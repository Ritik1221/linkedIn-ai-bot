"""
Caching utilities for the LinkedIn AI Agent.
This module provides functions for caching data using Redis.
"""

import json
import logging
from functools import wraps
from typing import Any, Callable, Dict, Optional, TypeVar, cast

import redis
from fastapi import Depends, Request

from src.app.core.config import settings

logger = logging.getLogger(__name__)

# Initialize Redis client
redis_client = redis.Redis.from_url(settings.REDIS_URL)

# Type variable for return type
T = TypeVar("T")


def get_cache_key(prefix: str, *args: Any, **kwargs: Any) -> str:
    """
    Generate a cache key from prefix and arguments.
    
    Args:
        prefix: Cache key prefix
        args: Positional arguments
        kwargs: Keyword arguments
        
    Returns:
        Cache key string
    """
    key_parts = [prefix]
    
    # Add positional arguments
    for arg in args:
        if arg is not None:
            key_parts.append(str(arg))
    
    # Add keyword arguments
    for k, v in sorted(kwargs.items()):
        if v is not None:
            key_parts.append(f"{k}:{v}")
    
    return ":".join(key_parts)


def cache_result(
    prefix: str, ttl: int = settings.CACHE_TTL, skip_args: int = 0
) -> Callable[[Callable[..., T]], Callable[..., T]]:
    """
    Decorator to cache function results in Redis.
    
    Args:
        prefix: Cache key prefix
        ttl: Time to live in seconds
        skip_args: Number of arguments to skip in key generation (e.g., self, request)
        
    Returns:
        Decorated function
    """
    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> T:
            # Skip specified number of arguments (e.g., self, request)
            cache_args = args[skip_args:]
            
            # Generate cache key
            cache_key = get_cache_key(prefix, *cache_args, **kwargs)
            
            # Try to get from cache
            cached_result = redis_client.get(cache_key)
            if cached_result:
                try:
                    return cast(T, json.loads(cached_result))
                except json.JSONDecodeError:
                    logger.warning(f"Failed to decode cached result for key: {cache_key}")
            
            # Call the original function
            result = func(*args, **kwargs)
            
            # Cache the result
            try:
                redis_client.setex(
                    cache_key,
                    ttl,
                    json.dumps(result, default=str)
                )
            except (TypeError, json.JSONDecodeError) as e:
                logger.warning(f"Failed to cache result for key {cache_key}: {str(e)}")
            
            return result
        
        return wrapper
    
    return decorator


def invalidate_cache(prefix: str, *args: Any, **kwargs: Any) -> None:
    """
    Invalidate cache for a specific key.
    
    Args:
        prefix: Cache key prefix
        args: Positional arguments
        kwargs: Keyword arguments
    """
    cache_key = get_cache_key(prefix, *args, **kwargs)
    redis_client.delete(cache_key)


def invalidate_cache_pattern(pattern: str) -> None:
    """
    Invalidate cache for all keys matching a pattern.
    
    Args:
        pattern: Redis key pattern (e.g., "user:*")
    """
    keys = redis_client.keys(pattern)
    if keys:
        redis_client.delete(*keys)


def get_redis_client() -> redis.Redis:
    """
    Get Redis client instance.
    
    Returns:
        Redis client
    """
    return redis_client 