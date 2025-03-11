"""
Rate limiting utilities for the LinkedIn AI Agent.
This module provides rate limiting functionality.
"""

import time
from datetime import datetime, timedelta
from typing import Any, Callable, Dict, List, Optional, Tuple, Union

from fastapi import Depends, HTTPException, Request, status
from redis.asyncio import Redis

from src.app.utils.cache import get_redis


class RateLimiter:
    """
    Rate limiter using Redis for storage.
    """
    
    def __init__(
        self,
        times: int = 5,
        seconds: int = 60,
        prefix: str = "rate_limit",
        redis: Optional[Redis] = None,
    ):
        """
        Initialize rate limiter.
        
        Args:
            times: Number of allowed requests in the time period
            seconds: Time period in seconds
            prefix: Redis key prefix
            redis: Redis connection (optional, will use get_redis() if not provided)
        """
        self.times = times
        self.seconds = seconds
        self.prefix = prefix
        self._redis = redis
    
    async def _get_redis(self) -> Redis:
        """
        Get Redis connection.
        """
        if self._redis is None:
            self._redis = await get_redis()
        return self._redis
    
    def _get_key(self, key: str) -> str:
        """
        Get Redis key.
        
        Args:
            key: Key identifier (typically IP address or user ID)
            
        Returns:
            Redis key string
        """
        return f"{self.prefix}:{key}"
    
    async def is_rate_limited(self, key: str) -> Tuple[bool, int, int]:
        """
        Check if a key is rate limited.
        
        Args:
            key: Key identifier (typically IP address or user ID)
            
        Returns:
            Tuple of (is_limited, current_count, ttl)
        """
        redis = await self._get_redis()
        redis_key = self._get_key(key)
        
        # Get current count
        count = await redis.get(redis_key)
        
        if count is None:
            # First request, set count to 1 with TTL
            await redis.set(redis_key, 1, ex=self.seconds)
            return False, 1, self.seconds
        
        # Increment count
        count = int(count)
        
        # Get TTL
        ttl = await redis.ttl(redis_key)
        
        # Check if over limit
        if count >= self.times:
            return True, count, ttl
        
        # Not over limit, increment count
        await redis.incr(redis_key)
        return False, count + 1, ttl
    
    async def reset(self, key: str) -> bool:
        """
        Reset rate limit for a key.
        
        Args:
            key: Key identifier (typically IP address or user ID)
            
        Returns:
            True if reset, False otherwise
        """
        redis = await self._get_redis()
        result = await redis.delete(self._get_key(key))
        return result > 0


def rate_limit(
    times: int = 5,
    seconds: int = 60,
    prefix: str = "rate_limit",
    key_func: Callable[[Request], str] = lambda request: request.client.host,
):
    """
    Rate limiting dependency.
    
    Args:
        times: Number of allowed requests in the time period
        seconds: Time period in seconds
        prefix: Redis key prefix
        key_func: Function to extract key from request
        
    Returns:
        Dependency function
    """
    limiter = RateLimiter(times=times, seconds=seconds, prefix=prefix)
    
    async def rate_limit_dependency(request: Request):
        key = key_func(request)
        is_limited, count, ttl = await limiter.is_rate_limited(key)
        
        if is_limited:
            # Add headers
            headers = {
                "X-RateLimit-Limit": str(times),
                "X-RateLimit-Remaining": "0",
                "X-RateLimit-Reset": str(int(time.time() + ttl)),
                "Retry-After": str(ttl),
            }
            
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail=f"Rate limit exceeded. Try again in {ttl} seconds.",
                headers=headers,
            )
        
        # Add rate limit headers to all responses
        request.state.rate_limit_headers = {
            "X-RateLimit-Limit": str(times),
            "X-RateLimit-Remaining": str(times - count),
            "X-RateLimit-Reset": str(int(time.time() + ttl)),
        }
        
        return True
    
    return Depends(rate_limit_dependency) 