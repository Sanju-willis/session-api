# src\services\session_service.py
from .thread_manager import ThreadManager
from src.core import LangGraphManager
from typing import Dict, Any, Optional
from src.utils import build_initial_state, persist_state, build_context
from pprint import pprint


class LangGraphService:
    def __init__(self):
        self.manager = LangGraphManager()
        self.thread_manager = ThreadManager()

    def create_session(
        self,
        user_id: str,
        company_id: str,
        module: str,
        thread_type: str,
        entity_id: str,
        item_id: str = None,
        parent_thread_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        # pprint(f"Thread info: {parent_thread_id}")

        thread_info = self.thread_manager.get_thread(
            user_id, company_id, module, thread_type, entity_id, item_id, parent_thread_id
        )
        pprint(f"Thread info: {thread_type}, {module}")

        context = build_context(thread_type.value, entity_id)

        # Pass thread_type directly, not inside context
        initial_state = build_initial_state(
            user_id,
            company_id,
            module.value,
            thread_type.value,  # Add this parameter
            context,
        )

        persist_state(thread_info.thread_id, initial_state)
        # pprint(f"Thread info: {initial_state}")
        stage = initial_state.get("stage") if isinstance(initial_state, dict) else initial_state.stage

        return {
            "session_id": thread_info.thread_id,
            "thread_type": thread_type,
            "module": module,
            "stage": stage,
            "parent_thread": thread_info.parent_thread_id,
            "entity_id": entity_id, 
            
        }
