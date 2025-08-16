# src\types_\conversation_type.py
from typing import Any, Optional
from langgraph.graph import MessagesState


class CustomState(MessagesState):
    user_id: str
    company_id: str
    module: str
    stage: str
    step: int
    thread_type: Optional[str]  # e.g., "company", "product", "service"
    context: Optional[dict[str, Any]]
    user_message: str = ""
    next_action: str = ""
