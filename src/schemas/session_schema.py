# src\schemas\session_schema.py
from pydantic import BaseModel
from typing import Optional
from src.types_ import Module, ThreadType

class StartSessionRequest(BaseModel):
    module: Module
    thread_type: ThreadType
    entity_id: Optional[str] = None
    parent_thread_id: Optional[str] = None 

    

class SessionResponse(BaseModel):
    session_id: str
    module: Optional[str] = None
    thread_type: str
    stage: str
    parent_thread: Optional[str] = None  
    entity_id: Optional[str] = None


class SendMessageIn(BaseModel):
    session_id: str
    message: str


class MessageOut(BaseModel):
    message: str
    message_type: str
    timestamp: str
    session_id: str
    stage: Optional[str] = "response"
    node: Optional[str] = "unknown"
