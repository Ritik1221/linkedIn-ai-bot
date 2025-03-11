"""
Networking service for the LinkedIn AI Agent.
This module provides functions for connection and message management.
"""

from datetime import datetime
from typing import Any, Dict, List, Optional, Union

from sqlalchemy import and_, or_, desc
from sqlalchemy.orm import Session

from src.app.models.user import User
from src.app.models.networking import Connection, Message
from src.app.schemas.networking import ConnectionCreate, ConnectionUpdate, MessageCreate, MessageUpdate


def get_connection(db: Session, connection_id: str) -> Optional[Connection]:
    """
    Get a connection by ID.
    
    Args:
        db: Database session
        connection_id: Connection ID
        
    Returns:
        Connection object if found, None otherwise
    """
    return db.query(Connection).filter(Connection.id == connection_id).first()


def get_connection_by_users(db: Session, user_id: str, connection_user_id: str) -> Optional[Connection]:
    """
    Get a connection between two users.
    
    Args:
        db: Database session
        user_id: User ID
        connection_user_id: Connection user ID
        
    Returns:
        Connection object if found, None otherwise
    """
    return db.query(Connection).filter(
        or_(
            and_(
                Connection.user_id == user_id,
                Connection.connection_user_id == connection_user_id
            ),
            and_(
                Connection.user_id == connection_user_id,
                Connection.connection_user_id == user_id
            )
        )
    ).first()


def get_connections_by_user(
    db: Session, user_id: str, skip: int = 0, limit: int = 100
) -> List[Connection]:
    """
    Get connections for a user with pagination.
    
    Args:
        db: Database session
        user_id: User ID
        skip: Number of connections to skip
        limit: Maximum number of connections to return
        
    Returns:
        List of connection objects
    """
    return (
        db.query(Connection)
        .filter(
            or_(
                Connection.user_id == user_id,
                Connection.connection_user_id == user_id
            )
        )
        .order_by(desc(Connection.created_at))
        .offset(skip)
        .limit(limit)
        .all()
    )


def create_connection(
    db: Session, connection_in: ConnectionCreate, user_id: str
) -> Connection:
    """
    Create a new connection.
    
    Args:
        db: Database session
        connection_in: Connection creation data
        user_id: User ID
        
    Returns:
        Created connection object
    """
    connection_data = connection_in.model_dump()
    connection_data["user_id"] = user_id
    connection_data["status"] = connection_data.get("status", "pending")
    
    db_connection = Connection(**connection_data)
    db.add(db_connection)
    db.commit()
    db.refresh(db_connection)
    return db_connection


def update_connection(
    db: Session, connection: Connection, connection_in: Union[ConnectionUpdate, Dict[str, Any]]
) -> Connection:
    """
    Update a connection.
    
    Args:
        db: Database session
        connection: Connection object to update
        connection_in: Connection update data
        
    Returns:
        Updated connection object
    """
    connection_data = connection.__dict__
    if isinstance(connection_in, dict):
        update_data = connection_in
    else:
        update_data = connection_in.model_dump(exclude_unset=True)
    
    # If status is changing, update the status_updated_at field
    if "status" in update_data and update_data["status"] != connection.status:
        update_data["status_updated_at"] = datetime.utcnow()
    
    for field in connection_data:
        if field in update_data:
            setattr(connection, field, update_data[field])
    
    db.add(connection)
    db.commit()
    db.refresh(connection)
    return connection


def delete_connection(db: Session, connection_id: str) -> Connection:
    """
    Delete a connection.
    
    Args:
        db: Database session
        connection_id: Connection ID
        
    Returns:
        Deleted connection object
    """
    connection = db.query(Connection).filter(Connection.id == connection_id).first()
    db.delete(connection)
    db.commit()
    return connection


def get_message(db: Session, message_id: str) -> Optional[Message]:
    """
    Get a message by ID.
    
    Args:
        db: Database session
        message_id: Message ID
        
    Returns:
        Message object if found, None otherwise
    """
    return db.query(Message).filter(Message.id == message_id).first()


def get_messages_by_connection(
    db: Session, connection_id: str, skip: int = 0, limit: int = 100
) -> List[Message]:
    """
    Get messages for a connection with pagination.
    
    Args:
        db: Database session
        connection_id: Connection ID
        skip: Number of messages to skip
        limit: Maximum number of messages to return
        
    Returns:
        List of message objects
    """
    return (
        db.query(Message)
        .filter(Message.connection_id == connection_id)
        .order_by(Message.sent_at)
        .offset(skip)
        .limit(limit)
        .all()
    )


def get_messages_between_users(
    db: Session, user_id: str, other_user_id: str, skip: int = 0, limit: int = 100
) -> List[Message]:
    """
    Get messages between two users with pagination.
    
    Args:
        db: Database session
        user_id: User ID
        other_user_id: Other user ID
        skip: Number of messages to skip
        limit: Maximum number of messages to return
        
    Returns:
        List of message objects
    """
    # Get the connection between the users
    connection = get_connection_by_users(db, user_id=user_id, connection_user_id=other_user_id)
    if not connection:
        return []
    
    return get_messages_by_connection(db, connection_id=str(connection.id), skip=skip, limit=limit)


def create_message(
    db: Session, message_in: MessageCreate, sender_id: str
) -> Message:
    """
    Create a new message.
    
    Args:
        db: Database session
        message_in: Message creation data
        sender_id: Sender user ID
        
    Returns:
        Created message object
    """
    message_data = message_in.model_dump()
    message_data["sender_id"] = sender_id
    message_data["sent_at"] = datetime.utcnow()
    message_data["is_read"] = False
    
    db_message = Message(**message_data)
    db.add(db_message)
    db.commit()
    db.refresh(db_message)
    return db_message


def update_message(
    db: Session, message: Message, message_in: Union[MessageUpdate, Dict[str, Any]]
) -> Message:
    """
    Update a message.
    
    Args:
        db: Database session
        message: Message object to update
        message_in: Message update data
        
    Returns:
        Updated message object
    """
    message_data = message.__dict__
    if isinstance(message_in, dict):
        update_data = message_in
    else:
        update_data = message_in.model_dump(exclude_unset=True)
    
    # If is_read is changing to True, update the read_at field
    if "is_read" in update_data and update_data["is_read"] and not message.is_read:
        update_data["read_at"] = datetime.utcnow()
    
    for field in message_data:
        if field in update_data:
            setattr(message, field, update_data[field])
    
    db.add(message)
    db.commit()
    db.refresh(message)
    return message


def delete_message(db: Session, message_id: str) -> Message:
    """
    Delete a message.
    
    Args:
        db: Database session
        message_id: Message ID
        
    Returns:
        Deleted message object
    """
    message = db.query(Message).filter(Message.id == message_id).first()
    db.delete(message)
    db.commit()
    return message


def mark_message_as_read(db: Session, message_id: str) -> Message:
    """
    Mark a message as read.
    
    Args:
        db: Database session
        message_id: Message ID
        
    Returns:
        Updated message object
    """
    message = get_message(db, message_id=message_id)
    if not message:
        return None
    
    return update_message(
        db, 
        message=message, 
        message_in={"is_read": True}
    )


def get_unread_message_count(db: Session, user_id: str) -> int:
    """
    Get the count of unread messages for a user.
    
    Args:
        db: Database session
        user_id: User ID
        
    Returns:
        Count of unread messages
    """
    # Get all connections for the user
    connections = get_connections_by_user(db, user_id=user_id)
    connection_ids = [str(conn.id) for conn in connections]
    
    # Count unread messages where the user is not the sender
    return (
        db.query(Message)
        .filter(
            Message.connection_id.in_(connection_ids),
            Message.sender_id != user_id,
            Message.is_read == False
        )
        .count()
    )


def get_connection_suggestions(db: Session, user_id: str, limit: int = 10) -> List[Dict[str, Any]]:
    """
    Get connection suggestions for a user.
    
    Args:
        db: Database session
        user_id: User ID
        limit: Maximum number of suggestions to return
        
    Returns:
        List of user objects with connection suggestion metadata
    """
    # Get existing connections
    existing_connections = get_connections_by_user(db, user_id=user_id)
    connected_user_ids = []
    
    for conn in existing_connections:
        if conn.user_id == user_id:
            connected_user_ids.append(conn.connection_user_id)
        else:
            connected_user_ids.append(conn.user_id)
    
    # Add the user's own ID to exclude from suggestions
    connected_user_ids.append(user_id)
    
    # Get users who are not already connected
    users = (
        db.query(User)
        .filter(User.id.notin_(connected_user_ids))
        .limit(limit)
        .all()
    )
    
    # Add suggestion metadata
    suggestions = []
    for user in users:
        # In a real implementation, you would calculate shared connections,
        # similar skills, etc. to provide more context for the suggestion
        suggestions.append({
            "user": user,
            "shared_connections": 0,  # Placeholder
            "similar_skills": [],  # Placeholder
            "suggestion_reason": "User you might know"  # Placeholder
        })
    
    return suggestions


def accept_connection_request(db: Session, connection_id: str) -> Connection:
    """
    Accept a connection request.
    
    Args:
        db: Database session
        connection_id: Connection ID
        
    Returns:
        Updated connection object
    """
    connection = get_connection(db, connection_id=connection_id)
    if not connection:
        return None
    
    return update_connection(
        db, 
        connection=connection, 
        connection_in={"status": "accepted"}
    )


def reject_connection_request(db: Session, connection_id: str) -> Connection:
    """
    Reject a connection request.
    
    Args:
        db: Database session
        connection_id: Connection ID
        
    Returns:
        Updated connection object
    """
    connection = get_connection(db, connection_id=connection_id)
    if not connection:
        return None
    
    return update_connection(
        db, 
        connection=connection, 
        connection_in={"status": "rejected"}
    )


def get_pending_connection_requests(db: Session, user_id: str) -> List[Connection]:
    """
    Get pending connection requests for a user.
    
    Args:
        db: Database session
        user_id: User ID
        
    Returns:
        List of pending connection objects
    """
    return (
        db.query(Connection)
        .filter(
            Connection.connection_user_id == user_id,
            Connection.status == "pending"
        )
        .all()
    )


def generate_connection_message(db: Session, user_id: str, connection_user_id: str, context: Optional[Dict[str, Any]] = None) -> str:
    """
    Generate a personalized connection message.
    
    Args:
        db: Database session
        user_id: User ID
        connection_user_id: Connection user ID
        context: Optional context for message generation
        
    Returns:
        Generated message text
    """
    # This is a placeholder for the LLM-based message generation
    # In a real implementation, this would call the LLM service
    
    # Get the users
    user = db.query(User).filter(User.id == user_id).first()
    connection_user = db.query(User).filter(User.id == connection_user_id).first()
    
    if not user or not connection_user:
        return "I'd like to connect with you on LinkedIn AI Agent."
    
    # Generate a simple message based on available information
    message = f"Hi {connection_user.full_name.split()[0]}, I'm {user.full_name}. "
    
    if context:
        if context.get("shared_connections"):
            message += f"We have {context.get('shared_connections')} connections in common. "
        
        if context.get("similar_skills"):
            skills = context.get("similar_skills")
            if len(skills) > 0:
                message += f"I noticed we both have experience with {', '.join(skills[:2])}. "
        
        if context.get("reason"):
            message += f"{context.get('reason')} "
    
    message += "I'd like to connect with you to expand our professional networks."
    
    return message 