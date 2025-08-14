# src\services\session_service.py
from src.services.thread_manager import ThreadManager
from src.core.langraph_config import LangGraphManager
from typing import Dict, Any
from src.utils.lang.langraph_utils import build_initial_state, persist_state


class LangGraphService:
    def __init__(self):
        self.manager = LangGraphManager()
        self.thread_manager = ThreadManager()

    def create_session(
        self, user_id: str, company_id: str, module: str, thread_type: str, item_id: str = None
    ) -> Dict[str, Any]:
        thread_info = self.thread_manager.get_thread(user_id, company_id, module, thread_type, item_id)
        context = self._build_context(thread_type, item_id)

        # Pass thread_type directly, not inside context
        initial_state = build_initial_state(
            user_id,
            company_id,
            module,
            thread_info.stage,
            thread_type,  # Add this parameter
            context,
        )

        persist_state(thread_info.thread_id, initial_state)

        return {
            "session_id": thread_info.thread_id,
            "thread_type": thread_type,
            "module": module,
            "stage": thread_info.stage,
            "parent_thread": thread_info.parent_thread_id,
            **({"item_id": item_id} if item_id else {}),
        }

    def _build_context(self, thread_type: str, item_id: str = None) -> Dict[str, Any]:
        # Remove thread_type from context since it's a direct field
        base = {}

        if thread_type == "company":
            base["sub_module"] = "company_profile"
        elif thread_type == "product":
            base["sub_module"] = "product"
            base["product_id"] = item_id
        elif thread_type == "service":
            base["sub_module"] = "service"
            base["service_id"] = item_id
        else:
            base["sub_module"] = thread_type  # fallback

        return base
