"""
Configuration settings for the LinkedIn AI Agent.
"""

import secrets
from typing import Any, Dict, List, Optional, Union

from pydantic import AnyHttpUrl, PostgresDsn, field_validator
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """
    Application settings.
    """
    # API settings
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = secrets.token_urlsafe(32)
    # 60 minutes * 24 hours * 8 days = 8 days
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8
    # 60 minutes * 24 hours * 30 days = 30 days
    REFRESH_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 30
    
    # Project info
    PROJECT_NAME: str = "LinkedIn AI Agent"
    PROJECT_DESCRIPTION: str = "AI-powered LinkedIn job search and networking assistant"
    VERSION: str = "0.1.0"
    
    # CORS settings
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []

    @field_validator("BACKEND_CORS_ORIGINS", mode="before")
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    # Database settings
    POSTGRES_SERVER: str = "localhost"
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = "postgres"
    POSTGRES_DB: str = "linkedin_agent"
    SQLALCHEMY_DATABASE_URI: Optional[PostgresDsn] = None

    @field_validator("SQLALCHEMY_DATABASE_URI", mode="before")
    def assemble_db_connection(cls, v: Optional[str], values: Dict[str, Any]) -> Any:
        if isinstance(v, str):
            return v
        return PostgresDsn.build(
            scheme="postgresql",
            username=values.data.get("POSTGRES_USER"),
            password=values.data.get("POSTGRES_PASSWORD"),
            host=values.data.get("POSTGRES_SERVER"),
            path=f"{values.data.get('POSTGRES_DB') or ''}",
        )

    # LinkedIn OAuth settings
    LINKEDIN_CLIENT_ID: str = ""
    LINKEDIN_CLIENT_SECRET: str = ""
    LINKEDIN_REDIRECT_URI: str = "http://localhost:3000/auth/linkedin/callback"

    # LLM settings
    LLM_PROVIDER: str = "anthropic"  # anthropic or openai
    LLM_MODEL: str = "claude-3-opus-20240229"  # claude-3-opus-20240229, gpt-4-turbo, etc.
    ANTHROPIC_API_KEY: str = ""
    OPENAI_API_KEY: str = ""
    
    # Vector database settings
    VECTOR_DB_PROVIDER: str = "pinecone"  # pinecone, qdrant, etc.
    PINECONE_API_KEY: str = ""
    PINECONE_ENVIRONMENT: str = ""
    PINECONE_INDEX_NAME: str = "linkedin-agent-index"

    # JWT settings
    JWT_SECRET: str = SECRET_KEY
    JWT_ALGORITHM: str = "HS256"

    # Email settings
    SMTP_TLS: bool = True
    SMTP_PORT: Optional[int] = None
    SMTP_HOST: Optional[str] = None
    SMTP_USER: Optional[str] = None
    SMTP_PASSWORD: Optional[str] = None
    EMAILS_FROM_EMAIL: Optional[str] = None
    EMAILS_FROM_NAME: Optional[str] = None

    # Celery settings
    CELERY_BROKER_URL: str = "redis://localhost:6379/0"
    CELERY_RESULT_BACKEND: str = "redis://localhost:6379/0"

    # Caching settings
    REDIS_URL: str = "redis://localhost:6379/1"
    CACHE_TTL: int = 3600  # 1 hour in seconds

    class Config:
        case_sensitive = True
        env_file = ".env"


settings = Settings() 