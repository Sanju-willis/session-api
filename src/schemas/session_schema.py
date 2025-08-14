# src\schemas\session_schema.py
from pydantic import BaseModel
from typing import Optional


class StartSessionRequest(BaseModel):
    module: str
    thread_type: str
    item_id: Optional[str] = None
    productId: Optional[str] = None  # Default to module, can be overridden


class SessionResponse(BaseModel):
    session_id: str
    module: Optional[str] = None
    thread_type: str
    stage: str
    parent_thread: Optional[str] = None  # Optional parent thread ID


class SendMessageIn(BaseModel):
    session_id: str
    message: str
    message_type: str = "user"


class MessageOut(BaseModel):
    message: str
    message_type: str
    timestamp: str
    session_id: str
