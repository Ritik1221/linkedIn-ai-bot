"""
Networking endpoints for the LinkedIn AI Agent.
"""

from typing import Any, Dict, List

from fastapi import APIRouter, Depends, HTTPException, status, Form
from sqlalchemy.orm import Session

from src.app.db.session import get_db
from src.app.models.user import User
from src.app.schemas.networking import Connection, ConnectionCreate, ConnectionUpdate, Message, MessageCreate
from src.app.services.networking import (
    create_connection,
    get_connection,
    get_connections_by_user,
    update_connection,
    delete_connection,
    get_connection_by_users,
    get_pending_connection_requests,
    accept_connection_request,
    reject_connection_request,
    get_connection_suggestions,
    create_message,
    get_message,
    get_messages_by_connection,
    get_messages_between_users,
    mark_message_as_read,
    get_unread_message_count,
    generate_connection_message
)
from src.app.services.user import get_current_active_user, get_user

router = APIRouter()


@router.get("/connections", response_model=List[Connection])
async def read_connections(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Retrieve user connections.
    """
    connections = get_connections_by_user(db, user_id=str(current_user.id), skip=skip, limit=limit)
    return connections


@router.post("/connections", response_model=Connection)
async def create_connection_request(
    connection_in: ConnectionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Create new connection request.
    """
    # Check if user exists
    user = get_user(db, user_id=connection_in.connection_user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    
    # Check if connection already exists
    existing_connection = get_connection_by_users(
        db, user_id=str(current_user.id), connection_user_id=connection_in.connection_user_id
    )
    if existing_connection:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Connection already exists",
        )
    
    connection = create_connection(
        db, connection_in=connection_in, user_id=str(current_user.id)
    )
    return connection


@router.get("/connection-requests", response_model=List[Connection])
async def read_connection_requests(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Retrieve pending connection requests for the current user.
    """
    connections = get_pending_connection_requests(db, user_id=str(current_user.id))
    return connections


@router.get("/connection-suggestions", response_model=List[Dict[str, Any]])
async def get_suggestions(
    limit: int = 10,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Get connection suggestions for the current user.
    """
    suggestions = get_connection_suggestions(db, user_id=str(current_user.id), limit=limit)
    return suggestions


@router.post("/connections/{connection_id}/accept", response_model=Connection)
async def accept_request(
    connection_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Accept a connection request.
    """
    connection = get_connection(db, connection_id=connection_id)
    if not connection:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Connection not found",
        )
    
    # Check if user is the connection recipient
    if str(connection.connection_user_id) != str(current_user.id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions",
        )
    
    connection = accept_connection_request(db, connection_id=connection_id)
    return connection


@router.post("/connections/{connection_id}/reject", response_model=Connection)
async def reject_request(
    connection_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Reject a connection request.
    """
    connection = get_connection(db, connection_id=connection_id)
    if not connection:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Connection not found",
        )
    
    # Check if user is the connection recipient
    if str(connection.connection_user_id) != str(current_user.id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions",
        )
    
    connection = reject_connection_request(db, connection_id=connection_id)
    return connection


@router.put("/connections/{connection_id}", response_model=Connection)
async def update_connection_details(
    connection_id: str,
    connection_in: ConnectionUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Update connection details.
    """
    connection = get_connection(db, connection_id=connection_id)
    if not connection:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Connection not found",
        )
    
    # Check if user is part of the connection
    if str(connection.user_id) != str(current_user.id) and str(connection.connection_user_id) != str(current_user.id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions",
        )
    
    connection = update_connection(db, connection=connection, connection_in=connection_in)
    return connection


@router.delete("/connections/{connection_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_connection_request(
    connection_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Delete a connection.
    """
    connection = get_connection(db, connection_id=connection_id)
    if not connection:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Connection not found",
        )
    
    # Check if user is part of the connection
    if str(connection.user_id) != str(current_user.id) and str(connection.connection_user_id) != str(current_user.id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions",
        )
    
    delete_connection(db, connection_id=connection_id)
    return None


@router.get("/messages/unread-count", response_model=int)
async def get_unread_messages_count(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Get the count of unread messages for the current user.
    """
    count = get_unread_message_count(db, user_id=str(current_user.id))
    return count


@router.get("/messages/connection/{connection_id}", response_model=List[Message])
async def read_messages_by_connection(
    connection_id: str,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Retrieve messages for a specific connection.
    """
    # Check if connection exists and user is part of it
    connection = get_connection(db, connection_id=connection_id)
    if not connection:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Connection not found",
        )
    
    if str(connection.user_id) != str(current_user.id) and str(connection.connection_user_id) != str(current_user.id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions",
        )
    
    messages = get_messages_by_connection(db, connection_id=connection_id, skip=skip, limit=limit)
    return messages


@router.get("/messages/user/{user_id}", response_model=List[Message])
async def read_messages_with_user(
    user_id: str,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Retrieve messages between the current user and another user.
    """
    # Check if user exists
    user = get_user(db, user_id=user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    
    messages = get_messages_between_users(
        db, user_id=str(current_user.id), other_user_id=user_id, skip=skip, limit=limit
    )
    return messages


@router.post("/messages", response_model=Message)
async def create_new_message(
    message_in: MessageCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Create new message.
    """
    # Check if connection exists and user is part of it
    connection = get_connection(db, connection_id=message_in.connection_id)
    if not connection:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Connection not found",
        )
    
    if str(connection.user_id) != str(current_user.id) and str(connection.connection_user_id) != str(current_user.id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions",
        )
    
    # Check if connection is active
    if connection.status != "accepted":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot send message to non-connected user",
        )
    
    message = create_message(
        db, message_in=message_in, sender_id=str(current_user.id)
    )
    return message


@router.post("/messages/{message_id}/read", response_model=Message)
async def mark_message_read(
    message_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Mark a message as read.
    """
    message = get_message(db, message_id=message_id)
    if not message:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Message not found",
        )
    
    # Get the connection to check permissions
    connection = get_connection(db, connection_id=message.connection_id)
    if not connection:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Connection not found",
        )
    
    # Check if user is part of the connection and is the recipient
    is_recipient = (
        (str(connection.user_id) == str(current_user.id) and str(message.sender_id) != str(current_user.id)) or
        (str(connection.connection_user_id) == str(current_user.id) and str(message.sender_id) != str(current_user.id))
    )
    
    if not is_recipient:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions",
        )
    
    updated_message = mark_message_as_read(db, message_id=message_id)
    return updated_message


@router.post("/generate-message", response_model=str)
async def generate_connection_request_message(
    user_id: str = Form(...),
    reason: str = Form(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Generate a personalized connection request message.
    """
    # Check if user exists
    user = get_user(db, user_id=user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    
    context = {}
    if reason:
        context["reason"] = reason
    
    message = generate_connection_message(
        db, user_id=str(current_user.id), connection_user_id=user_id, context=context
    )
    return message 