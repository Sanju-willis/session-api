# src\utils\lang\state_persistence.py
from typing import Dict, Any
from src.core.langraph_config import LangGraphManager
from src.utils.logging import setup_logging

logger = setup_logging(__name__)

def update_partial_state(session_id: str, state: Dict[str, Any]) -> None:
    """Update existing LangGraph state from a dict"""
    try:
        config = {"configurable": {"thread_id": session_id}}

        clean_state = {
            "user_id": state.get("user_id"),
            "company_id": state.get("company_id"),
            "module": state.get("module"),
            "stage": state.get("stage"),
            "step": state.get("step", 1),
            "messages": state.get("messages", []),
            "next_action": state.get("next_action", ""),
        }

        manager = LangGraphManager()
        with manager.get_app() as app:
            app.update_state(config, clean_state)
    except Exception as e:
        logger.warning(f"[BaseGraph] Failed to update state for session {session_id}: {e}")
