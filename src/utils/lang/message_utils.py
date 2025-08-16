# src\utils\lang\message_utils.py
from typing import Dict, Any, List
from datetime import datetime, timezone


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def append_message(
    state: Dict[str, Any], role: str, content: str, node: str = None, message_type: str = None
) -> Dict[str, Any]:
    """Add a message to state['messages'] with timestamp and return cleaned state."""
    messages: List[Dict[str, Any]] = state.get("messages", [])
    messages.append(
        {
            "role": role,
            "content": content,
            "timestamp": _now(),
        }
    )

    # Create clean state
    clean_state = state.copy()
    clean_state["messages"] = messages
    clean_state["message"] = content

    # Add optional fields
    if message_type:
        clean_state["message_type"] = message_type
    if node:
        clean_state["node"] = node

    return clean_state

   
