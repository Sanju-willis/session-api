# src\utils\lang\message_utils.py
from typing import Dict, Any, List
from datetime import datetime, timezone


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def append_message(state: Dict[str, Any], role: str, content: str) -> Dict[str, Any]:
    """Add a message to state['messages'] with timestamp and return cleaned state."""
    messages: List[Dict[str, Any]] = state.get("messages", [])
    messages.append({
        "role": role,
        "content": content,
        "timestamp": _now(),
    })

    return {
        "user_id": state.get("user_id"),
        "company_id": state.get("company_id"),
        "module": state.get("module"),
        "stage": state.get("stage"),
        "step": state.get("step", 1),
        "messages": messages,
        "next_action": state.get("next_action", ""),
    }
