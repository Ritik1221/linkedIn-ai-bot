"""
Database session management for the LinkedIn AI Agent.
"""

from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from src.app.core.config import settings

# Create SQLAlchemy engine
engine = create_engine(
    settings.SQLALCHEMY_DATABASE_URI,
    pool_pre_ping=True,
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