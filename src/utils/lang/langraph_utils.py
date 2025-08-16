# src\utils\lang\langraph_utils.py
from src.types_ import ConversationState
from typing import Dict, Any, Optional
from src.core import LangGraphManager
from src.utils import setup_logging


logger = setup_logging(__name__)


def build_initial_state(
    user_id: str, company_id: str, module: str, thread_type: str, context: Dict[str, Any] = None
) -> ConversationState:
    # Determine stage based on business logic
    if thread_type == "module" and module == "home":
        stage = "onboarded"
    elif thread_type == "company":
        stage = "need_company"
    elif thread_type == "product":
        stage = "company_completed"
    else:
        stage = "onboarded"

    return ConversationState(
        user_id=user_id,
        company_id=company_id,
        module=module,
        thread_type=thread_type,
        messages=[],
        stage=stage, 
        step=1,
        context=context or {},
    )


def persist_state(thread_id: str, state: ConversationState) -> None:
    #print(f"Persisting state for thread {thread_id}: {state}")
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


def update_partial_state(session_id: str, state: Dict[str, Any]) -> None:
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
