# src\utils\lang\langraph_utils.py
from src.types_.conversation_type import ConversationState
from typing import Dict, Any, Optional
from src.core.langraph_config import LangGraphManager
from src.utils.logging import setup_logging

logger = setup_logging(__name__)


def build_initial_state(
    user_id: str, company_id: str, module: str, stage: str, context: Dict[str, Any] = None
) -> ConversationState:
    return ConversationState(
        user_id=user_id,
        company_id=company_id,
        module=module,
        messages=[],
        stage=stage,
        step=1,
        context=context or {},
    )


def persist_state(thread_id: str, state: ConversationState) -> None:

    config = {"configurable": {"thread_id": thread_id}}
    manager = LangGraphManager()
    with manager.get_app() as app:
        app.invoke(state, config=config)


def get_session_state(session_id: str) -> Optional[Dict[str, Any]]:
    try:
        manager = LangGraphManager()
        config = {"configurable": {"thread_id": session_id}}
        with manager.get_app() as app:
            current_state = app.get_state(config)

        if current_state and current_state.values:
            vals = current_state.values
            return {
                "module": vals.get("module"),
                "stage": vals.get("stage"),
                "step": vals.get("step"),
                "user_id": vals.get("user_id"),
                "company_id": vals.get("company_id"),
                "context": vals.get("context", {}),
                "messages": vals.get("messages", []),
                "next_action": vals.get("next_action", ""),
            }
        return None
    except Exception as e:
        logger.warning(f"Could not retrieve state for session {session_id}: {e}")
        return None
