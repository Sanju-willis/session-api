# src\types\conversation_type.py
from typing_extensions import TypedDict
from typing import List, Any, Optional

class ConversationState(TypedDict):
    user_id: str
    company_id: str
    module: str
    messages: List[dict[str, Any]]
    stage: str
    step: int
    context: Optional[dict[str, Any]]