# src\graphs\nodes\onboarding_node.py
from typing import Dict, Any
from src.utils import append_message


def onboarding_node(state: Dict[str, Any]) -> Dict[str, Any]:
    """Welcome message for new users"""
    message = "Welcome to Kordor"

    # Update state with message and append to conversation
    return append_message(state, "assistant", message, node="onboarding_agent", message_type="assistant")
