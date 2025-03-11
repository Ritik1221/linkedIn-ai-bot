"""
Caching utilities for the LinkedIn AI Agent.
This module provides functions for efficient application-level caching.
"""

import json
import logging
from typing import Any, Dict, Optional, TypeVar, Union, cast

import redis.asyncio as redis
from fastapi import Depends

from src.app.core.config import settings

logger = logging.getLogger(__name__)

T = TypeVar("T")

# Initialize Redis connection
redis_client = redis.from_url(
    settings.REDIS_URL,
    encoding="utf-8",
    decode_responses=True,
)


async def get_redis() -> redis.Redis:
    """
    Get Redis client.
    
    Returns:
        Redis client
    """
    return redis_client


async def get_cached_data(
    key: str, 
    ttl: int = 3600, 
    cache_client: redis.Redis = Depends(get_redis)
) -> Optional[Dict[str, Any]]:
    """
    Get data from cache. If not present, return None.
    
    Args:
        key: Cache key
        ttl: Time to live in seconds (not used for retrieval, only for documentation)
        cache_client: Redis client
        
    Returns:
        Cached data or None if not found
    """
    try:
        cached = await cache_client.get(key)
        if cached:
            return json.loads(cached)
        return None
    except Exception as e:
        logger.error(f"Error retrieving from cache: {str(e)}")
        return None


async def set_cached_data(
    key: str,
    data: Any,
    ttl: int = 3600,
    cache_client: redis.Redis = Depends(get_redis)
) -> bool:
    """
    Set data in cache with TTL.
    
    Args:
        key: Cache key
        data: Data to cache
        ttl: Time to live in seconds
        cache_client: Redis client
        
    Returns:
        True if successfully cached, False otherwise
    """
    try:
        await cache_client.set(key, json.dumps(data), ex=ttl)
        return True
    except Exception as e:
        logger.error(f"Error setting cache: {str(e)}")
        return False


async def invalidate_cache(
    key: str,
    cache_client: redis.Redis = Depends(get_redis)
) -> bool:
    """
    Invalidate cache for a specific key.
    
    Args:
        key: Cache key
        cache_client: Redis client
        
    Returns:
        True if successfully invalidated, False otherwise
    """
    try:
        await cache_client.delete(key)
        return True
    except Exception as e:
        logger.error(f"Error invalidating cache: {str(e)}")
        return False


async def invalidate_pattern(
    pattern: str,
    cache_client: redis.Redis = Depends(get_redis)
) -> bool:
    """
    Invalidate cache for all keys matching a pattern.
    
    Args:
        pattern: Pattern to match cache keys
        cache_client: Redis client
        
    Returns:
        True if successfully invalidated, False otherwise
    """
    try:
        keys = await cache_client.keys(pattern)
        if keys:
            await cache_client.delete(*keys)
        return True
    except Exception as e:
        logger.error(f"Error invalidating cache pattern: {str(e)}")
        return False


# Decorator for caching function results
def cache_result(key_prefix: str, ttl: int = 3600):
    """
    Decorator for caching function results.
    
    Args:
        key_prefix: Prefix for cache key
        ttl: Time to live in seconds
        
    Returns:
        Decorated function
    """
    def decorator(func):
        async def wrapper(*args, **kwargs):
            # Generate cache key from function name, args, and kwargs
            key_parts = [key_prefix, func.__name__]
            for arg in args:
                key_parts.append(str(arg))
            for k, v in sorted(kwargs.items()):
                key_parts.append(f"{k}:{v}")
            cache_key = ":".join(key_parts)
            
            # Try to get from cache first
            cache_client = await get_redis()
            cached_data = await get_cached_data(cache_key, ttl, cache_client)
            if cached_data is not None:
                return cached_data
                
            # If not in cache, call the function
            result = await func(*args, **kwargs)
            
            # Cache the result
            await set_cached_data(cache_key, result, ttl, cache_client)
            
            return result
        return wrapper
    return decorator 