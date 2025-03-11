"""
Database session management for the LinkedIn AI Agent.
"""

from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from src.app.core.config import settings

# Create SQLAlchemy engine with optimized connection pooling
engine = create_engine(
    settings.SQLALCHEMY_DATABASE_URI,
    pool_size=20,
    max_overflow=10,
    pool_pre_ping=True,
    pool_recycle=3600,
)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create base class for models
Base = declarative_base()


def get_db() -> Generator:
    """
    Get database session.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close() 