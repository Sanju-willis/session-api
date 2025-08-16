# src\types_\conversation_type.py
from typing_extensions import TypedDict
from typing import List, Any, Optional
from langgraph.graph import MessagesState

class ConversationState(TypedDict):
    session_id: str = ""
    user_id: str
    company_id: str
    module: str
    messages: List[dict[str, Any]]
    stage: str
    step: int
    thread_type: Optional[str]  # e.g., "company", "product", "service"
    context: Optional[dict[str, Any]]

class CustomState(MessagesState):
    session_id: str = ""
    user_message: str = ""
    module: str = ""
    stage: str = ""
    next_action: str = ""
    user_id: str = ""
    company_id: str = ""


