"""
Database index management utilities for the LinkedIn AI Agent.
This module provides functions for creating and managing database indexes.
"""

import logging
from typing import List, Optional, Tuple

from sqlalchemy import Column, Index, MetaData, Table, create_engine, inspect, text
from sqlalchemy.engine import Engine
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.schema import CreateIndex

from src.app.core.config import settings
from src.app.db.base import Base

logger = logging.getLogger(__name__)


def get_engine() -> Engine:
    """
    Get SQLAlchemy engine instance.
    
    Returns:
        SQLAlchemy engine
    """
    return create_engine(settings.SQLALCHEMY_DATABASE_URI)


def get_existing_indexes(engine: Engine, table_name: str) -> List[str]:
    """
    Get existing indexes for a table.
    
    Args:
        engine: SQLAlchemy engine
        table_name: Table name
        
    Returns:
        List of index names
    """
    inspector = inspect(engine)
    return [idx["name"] for idx in inspector.get_indexes(table_name)]


def create_index(
    engine: Engine, table_name: str, column_names: List[str], index_name: Optional[str] = None, unique: bool = False
) -> bool:
    """
    Create an index on a table.
    
    Args:
        engine: SQLAlchemy engine
        table_name: Table name
        column_names: Column names to include in the index
        index_name: Index name (auto-generated if None)
        unique: Whether the index should be unique
        
    Returns:
        True if index was created, False otherwise
    """
    if not index_name:
        index_name = f"idx_{table_name}_{'_'.join(column_names)}"
    
    # Check if index already exists
    existing_indexes = get_existing_indexes(engine, table_name)
    if index_name in existing_indexes:
        logger.info(f"Index {index_name} already exists on table {table_name}")
        return False
    
    try:
        # Create index
        columns_str = ", ".join(column_names)
        unique_str = "UNIQUE" if unique else ""
        with engine.begin() as conn:
            conn.execute(text(f"CREATE {unique_str} INDEX {index_name} ON {table_name} ({columns_str})"))
        
        logger.info(f"Created index {index_name} on table {table_name} ({columns_str})")
        return True
    except SQLAlchemyError as e:
        logger.error(f"Failed to create index {index_name} on table {table_name}: {str(e)}")
        return False


def create_composite_index(
    engine: Engine, table_name: str, column_names: List[str], index_name: Optional[str] = None, unique: bool = False
) -> bool:
    """
    Create a composite index on a table.
    
    Args:
        engine: SQLAlchemy engine
        table_name: Table name
        column_names: Column names to include in the index
        index_name: Index name (auto-generated if None)
        unique: Whether the index should be unique
        
    Returns:
        True if index was created, False otherwise
    """
    return create_index(engine, table_name, column_names, index_name, unique)


def create_text_search_index(
    engine: Engine, table_name: str, column_name: str, index_name: Optional[str] = None
) -> bool:
    """
    Create a full-text search index on a table column.
    
    Args:
        engine: SQLAlchemy engine
        table_name: Table name
        column_name: Column name to index
        index_name: Index name (auto-generated if None)
        
    Returns:
        True if index was created, False otherwise
    """
    if not index_name:
        index_name = f"idx_{table_name}_{column_name}_fts"
    
    # Check if index already exists
    existing_indexes = get_existing_indexes(engine, table_name)
    if index_name in existing_indexes:
        logger.info(f"Index {index_name} already exists on table {table_name}")
        return False
    
    try:
        # Create GIN index for full-text search
        with engine.begin() as conn:
            conn.execute(text(f"CREATE INDEX {index_name} ON {table_name} USING GIN (to_tsvector('english', {column_name}))"))
        
        logger.info(f"Created full-text search index {index_name} on table {table_name}.{column_name}")
        return True
    except SQLAlchemyError as e:
        logger.error(f"Failed to create full-text search index {index_name} on table {table_name}: {str(e)}")
        return False


def create_standard_indexes() -> None:
    """
    Create standard indexes for all tables.
    """
    engine = get_engine()
    
    # User indexes
    create_index(engine, "user", ["email"], unique=True)
    create_index(engine, "user", ["linkedin_id"], unique=True)
    
    # Profile indexes
    create_index(engine, "profile", ["user_id"], unique=True)
    create_index(engine, "profile", ["linkedin_profile_id"], unique=True)
    create_text_search_index(engine, "profile", "headline")
    create_text_search_index(engine, "profile", "summary")
    
    # Experience indexes
    create_index(engine, "experience", ["profile_id"])
    create_index(engine, "experience", ["linkedin_experience_id"], unique=True)
    create_text_search_index(engine, "experience", "title")
    create_text_search_index(engine, "experience", "company")
    
    # Education indexes
    create_index(engine, "education", ["profile_id"])
    create_index(engine, "education", ["linkedin_education_id"], unique=True)
    
    # Certification indexes
    create_index(engine, "certification", ["profile_id"])
    create_index(engine, "certification", ["linkedin_certification_id"], unique=True)
    
    # Skill indexes
    create_index(engine, "skill", ["profile_id"])
    create_index(engine, "skill", ["name", "profile_id"], unique=True)
    
    # Job indexes
    create_index(engine, "job", ["posted_by"])
    create_index(engine, "job", ["linkedin_job_id"], unique=True)
    create_text_search_index(engine, "job", "title")
    create_text_search_index(engine, "job", "description")
    create_composite_index(engine, "job", ["title", "company"])
    
    # Add GIN index for job skills
    try:
        with engine.begin() as conn:
            conn.execute(text("CREATE INDEX IF NOT EXISTS idx_jobs_skills ON job USING GIN (required_skills)"))
        logger.info("Created GIN index on job.required_skills")
    except SQLAlchemyError as e:
        logger.error(f"Failed to create GIN index on job.required_skills: {str(e)}")
    
    # Application indexes
    create_index(engine, "application", ["user_id"])
    create_index(engine, "application", ["job_id"])
    create_composite_index(engine, "application", ["user_id", "job_id"], unique=True)
    create_index(engine, "application", ["status"])
    
    # Connection indexes
    create_index(engine, "connection", ["user_id"])
    create_index(engine, "connection", ["connection_user_id"])
    create_composite_index(engine, "connection", ["user_id", "connection_user_id"], unique=True)
    create_index(engine, "connection", ["status"])
    
    # Message indexes
    create_index(engine, "message", ["connection_id"])
    create_index(engine, "message", ["sender_id"])
    create_composite_index(engine, "message", ["connection_id", "sent_at"])
    create_index(engine, "message", ["is_read"])


def optimize_database() -> None:
    """
    Perform database optimization tasks.
    """
    engine = get_engine()
    
    try:
        # Create standard indexes
        create_standard_indexes()
        
        # Analyze tables for query optimization
        with engine.begin() as conn:
            conn.execute(text("ANALYZE"))
        
        logger.info("Database optimization completed successfully")
    except SQLAlchemyError as e:
        logger.error(f"Database optimization failed: {str(e)}")


if __name__ == "__main__":
    # Run database optimization when script is executed directly
    optimize_database() 