"""
Main application module for the LinkedIn AI Agent.
"""

import logging
import os
from typing import Any

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.responses import JSONResponse

from src.app.api.v1.router import api_router
from src.app.core.config import settings
from src.app.utils.logging import setup_logging, get_logger
from src.app.utils.middleware import RequestTimingMiddleware, RateLimitHeadersMiddleware

# Configure structured logging
setup_logging(
    log_level=settings.LOG_LEVEL,
    json_format=settings.JSON_LOGS,
    console_output=True,
    file_output=settings.LOG_TO_FILE,
    log_file=settings.LOG_FILE_PATH,
)

logger = get_logger(__name__)


def create_application() -> FastAPI:
    """
    Create FastAPI application.
    """
    application = FastAPI(
        title=settings.PROJECT_NAME,
        description=settings.PROJECT_DESCRIPTION,
        version=settings.VERSION,
        openapi_url=f"{settings.API_V1_STR}/openapi.json",
        docs_url=f"{settings.API_V1_STR}/docs",
        redoc_url=f"{settings.API_V1_STR}/redoc",
    )

    # Set all CORS enabled origins
    if settings.BACKEND_CORS_ORIGINS:
        application.add_middleware(
            CORSMiddleware,
            allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )
    
    # Add GZip compression middleware
    application.add_middleware(GZipMiddleware, minimum_size=1000)
    
    # Add request timing middleware
    application.add_middleware(
        RequestTimingMiddleware,
        log_slow_responses=True,
        slow_response_threshold=0.5,
    )
    
    # Add rate limit headers middleware
    application.add_middleware(RateLimitHeadersMiddleware)

    # Include API router
    application.include_router(api_router, prefix=settings.API_V1_STR)

    @application.get("/")
    async def root() -> Any:
        """
        Root endpoint.
        """
        return {"message": "Welcome to the LinkedIn AI Agent API"}

    @application.get("/health")
    async def health() -> Any:
        """
        Health check endpoint.
        """
        return {"status": "ok"}

    @application.exception_handler(Exception)
    async def global_exception_handler(request: Request, exc: Exception) -> JSONResponse:
        """
        Global exception handler.
        """
        logger.error("unhandled_exception", exc_info=True, request_path=request.url.path)
        return JSONResponse(
            status_code=500,
            content={"detail": "Internal server error"},
        )

    return application


app = create_application()

# Startup event
@app.on_event("startup")
async def startup_event():
    """Application startup event."""
    logger.info("application_startup", environment=settings.ENVIRONMENT)
    # Initialize connections and resources
    
    # Create logs directory if it doesn't exist
    os.makedirs("logs", exist_ok=True)

# Shutdown event
@app.on_event("shutdown")
async def shutdown_event():
    """Application shutdown event."""
    logger.info("application_shutdown")
    # Clean up connections and resources

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("src.app.main:app", host="0.0.0.0", port=8000, reload=True) 