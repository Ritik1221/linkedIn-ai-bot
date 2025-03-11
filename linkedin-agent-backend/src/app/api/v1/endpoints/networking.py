"""
Networking endpoints for the LinkedIn AI Agent.
"""

from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.app.db.session import get_db
from src.app.schemas.connection import Connection, ConnectionCreate, ConnectionUpdate
from src.app.schemas.message import Message, MessageCreate
# from src.app.services.connection import create_connection, get_connection, get_connections, update_connection
# from src.app.services.message import create_message, get_messages
# from src.app.services.user import get_current_active_user

router = APIRouter()


@router.get("/connections", response_model=List[Connection])
async def read_connections(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    # current_user = Depends(get_current_active_user),
) -> Any:
    """
    Retrieve user connections.
    """
    # Uncomment when connection service is implemented
    # connections = get_connections(db, user_id=current_user.id, skip=skip, limit=limit)
    
    # For now, return a placeholder list of connections
    return [
        {
            "id": "00000000-0000-0000-0000-000000000000",
            "user_id": "00000000-0000-0000-0000-000000000000",
            "connected_user_id": "11111111-1111-1111-1111-111111111111",
            "status": "connected",
            "created_at": "2023-01-01T00:00:00",
            "updated_at": "2023-01-01T00:00:00",
        }
    ]


@router.post("/connections", response_model=Connection)
async def create_connection_request(
    connection_in: ConnectionCreate,
    db: Session = Depends(get_db),
    # current_user = Depends(get_current_active_user),
) -> Any:
    """
    Create new connection request.
    """
    # Uncomment when connection service is implemented
    # # Check if user exists
    # user = get_user_by_id(db, id=connection_in.connected_user_id)
    # if not user:
    #     raise HTTPException(
    #         status_code=status.HTTP_404_NOT_FOUND,
    #         detail="User not found",
    #     )
    # # Check if connection already exists
    # existing_connection = get_connection_by_users(
    #     db, user_id=current_user.id, connected_user_id=connection_in.connected_user_id
    # )
    # if existing_connection:
    #     raise HTTPException(
    #         status_code=status.HTTP_400_BAD_REQUEST,
    #         detail="Connection already exists",
    #     )
    # connection = create_connection(
    #     db, user_id=current_user.id, connected_user_id=connection_in.connected_user_id
    # )
    
    # For now, return a placeholder connection
    return {
        "id": "00000000-0000-0000-0000-000000000000",
        "user_id": "00000000-0000-0000-0000-000000000000",
        "connected_user_id": connection_in.connected_user_id,
        "status": "pending",
        "created_at": "2023-01-01T00:00:00",
        "updated_at": "2023-01-01T00:00:00",
    }


@router.get("/connection-requests", response_model=List[Connection])
async def read_connection_requests(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    # current_user = Depends(get_current_active_user),
) -> Any:
    """
    Retrieve pending connection requests for the current user.
    """
    # Uncomment when connection service is implemented
    # connections = get_connection_requests(db, user_id=current_user.id, skip=skip, limit=limit)
    
    # For now, return a placeholder list of connection requests
    return [
        {
            "id": "00000000-0000-0000-0000-000000000000",
            "user_id": "11111111-1111-1111-1111-111111111111",
            "connected_user_id": "00000000-0000-0000-0000-000000000000",
            "status": "pending",
            "created_at": "2023-01-01T00:00:00",
            "updated_at": "2023-01-01T00:00:00",
        }
    ]


@router.put("/connections/{connection_id}", response_model=Connection)
async def update_connection_status(
    connection_id: str,
    connection_in: ConnectionUpdate,
    db: Session = Depends(get_db),
    # current_user = Depends(get_current_active_user),
) -> Any:
    """
    Update connection status (accept or reject).
    """
    # Uncomment when connection service is implemented
    # connection = get_connection(db, id=connection_id)
    # if not connection:
    #     raise HTTPException(
    #         status_code=status.HTTP_404_NOT_FOUND,
    #         detail="Connection not found",
    #     )
    # # Check if user is the connection recipient
    # if connection.connected_user_id != current_user.id:
    #     raise HTTPException(
    #         status_code=status.HTTP_403_FORBIDDEN,
    #         detail="Not enough permissions",
    #     )
    # connection = update_connection(db, connection=connection, connection_in=connection_in)
    
    # For now, return a placeholder updated connection
    return {
        "id": connection_id,
        "user_id": "11111111-1111-1111-1111-111111111111",
        "connected_user_id": "00000000-0000-0000-0000-000000000000",
        "status": connection_in.status,
        "created_at": "2023-01-01T00:00:00",
        "updated_at": "2023-01-01T00:00:00",
    }


@router.get("/messages/{connection_id}", response_model=List[Message])
async def read_messages(
    connection_id: str,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    # current_user = Depends(get_current_active_user),
) -> Any:
    """
    Retrieve messages for a specific connection.
    """
    # Uncomment when message service is implemented
    # # Check if connection exists and user is part of it
    # connection = get_connection(db, id=connection_id)
    # if not connection:
    #     raise HTTPException(
    #         status_code=status.HTTP_404_NOT_FOUND,
    #         detail="Connection not found",
    #     )
    # if connection.user_id != current_user.id and connection.connected_user_id != current_user.id:
    #     raise HTTPException(
    #         status_code=status.HTTP_403_FORBIDDEN,
    #         detail="Not enough permissions",
    #     )
    # messages = get_messages(db, connection_id=connection_id, skip=skip, limit=limit)
    
    # For now, return a placeholder list of messages
    return [
        {
            "id": "00000000-0000-0000-0000-000000000000",
            "connection_id": connection_id,
            "sender_id": "11111111-1111-1111-1111-111111111111",
            "content": "Hello, how are you?",
            "created_at": "2023-01-01T00:00:00",
        },
        {
            "id": "22222222-2222-2222-2222-222222222222",
            "connection_id": connection_id,
            "sender_id": "00000000-0000-0000-0000-000000000000",
            "content": "I'm doing well, thank you!",
            "created_at": "2023-01-01T00:05:00",
        }
    ]


@router.post("/messages", response_model=Message)
async def create_new_message(
    message_in: MessageCreate,
    db: Session = Depends(get_db),
    # current_user = Depends(get_current_active_user),
) -> Any:
    """
    Create new message.
    """
    # Uncomment when message service is implemented
    # # Check if connection exists and user is part of it
    # connection = get_connection(db, id=message_in.connection_id)
    # if not connection:
    #     raise HTTPException(
    #         status_code=status.HTTP_404_NOT_FOUND,
    #         detail="Connection not found",
    #     )
    # if connection.user_id != current_user.id and connection.connected_user_id != current_user.id:
    #     raise HTTPException(
    #         status_code=status.HTTP_403_FORBIDDEN,
    #         detail="Not enough permissions",
    #     )
    # # Check if connection is active
    # if connection.status != "connected":
    #     raise HTTPException(
    #         status_code=status.HTTP_400_BAD_REQUEST,
    #         detail="Cannot send message to non-connected user",
    #     )
    # message = create_message(
    #     db, message_in=message_in, sender_id=current_user.id
    # )
    
    # For now, return a placeholder message
    return {
        "id": "33333333-3333-3333-3333-333333333333",
        "connection_id": message_in.connection_id,
        "sender_id": "00000000-0000-0000-0000-000000000000",
        "content": message_in.content,
        "created_at": "2023-01-01T00:10:00",
    } 