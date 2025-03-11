"""
Middleware utilities for the LinkedIn AI Agent.
This module provides middleware for request processing.
"""

import time
import logging
from typing import Callable

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import ASGIApp

logger = logging.getLogger(__name__)


class RequestTimingMiddleware(BaseHTTPMiddleware):
    """
    Middleware for tracking request timing and logging performance metrics.
    """
    
    def __init__(
        self,
        app: ASGIApp,
        log_slow_responses: bool = True,
        slow_response_threshold: float = 0.5,
    ):
        """
        Initialize middleware.
        
        Args:
            app: ASGI application
            log_slow_responses: Whether to log slow responses
            slow_response_threshold: Threshold in seconds for slow responses
        """
        super().__init__(app)
        self.log_slow_responses = log_slow_responses
        self.slow_response_threshold = slow_response_threshold
    
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        """
        Process request and log timing information.
        
        Args:
            request: HTTP request
            call_next: Next middleware or endpoint in chain
            
        Returns:
            HTTP response
        """
        start_time = time.time()
        
        # Process request
        response = await call_next(request)
        
        # Calculate processing time
        process_time = time.time() - start_time
        
        # Add timing header
        response.headers["X-Process-Time"] = str(process_time)
        
        # Log request processing time
        log_data = {
            "path": request.url.path,
            "method": request.method,
            "processing_time": process_time,
            "status_code": response.status_code,
        }
        
        # Log detailed info for slow responses
        if self.log_slow_responses and process_time > self.slow_response_threshold:
            logger.warning(
                f"Slow response detected: {process_time:.4f}s",
                extra=log_data
            )
        else:
            logger.info(
                f"Request processed in {process_time:.4f}s",
                extra=log_data
            )
        
        return response


class RateLimitHeadersMiddleware(BaseHTTPMiddleware):
    """
    Middleware for adding rate limit headers to responses.
    """
    
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        """
        Process request and add rate limit headers to response.
        
        Args:
            request: HTTP request
            call_next: Next middleware or endpoint in chain
            
        Returns:
            HTTP response
        """
        # Process request
        response = await call_next(request)
        
        # Add rate limit headers if available in request state
        if hasattr(request.state, "rate_limit_headers"):
            for header_name, header_value in request.state.rate_limit_headers.items():
                response.headers[header_name] = str(header_value)
        
        return response 