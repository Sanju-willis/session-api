# src\services\session_service.py
from src.services.thread_manager import ThreadManager
from src.core.langraph_config import LangGraphManager
from typing import Dict, Any
from src.utils import build_initial_state, persist_state


class LangGraphService:
    def __init__(self):
        self.manager = LangGraphManager()
        self.thread_manager = ThreadManager()

    def create_session(
        self, user_id: str, company_id: str, module: str, thread_type: str, item_id: str = None
    ) -> Dict[str, Any]:
        thread_info = self.thread_manager.get_thread(user_id, company_id, module, thread_type, item_id)

        # Build context based on thread type
        context = {}
        if thread_type == "company":
            context = {"sub_module": "company_profile"}
        elif thread_type == "product":
            context = {"sub_module": "product", "product_id": item_id}
        elif thread_type == "service":
            context = {"sub_module": "service", "service_id": item_id}

        initial_state = build_initial_state(user_id, company_id, module, thread_info.stage, context)
        persist_state(thread_info.thread_id, initial_state)

        return {
            "session_id": thread_info.thread_id,
            "thread_type": thread_type,
            "module": module,
            "stage": thread_info.stage,
            "next_action": self._get_next_action(module, thread_info.stage, thread_type),
            "parent_thread": thread_info.parent_thread_id,
            **({"item_id": item_id} if item_id else {}),
        }

    def _get_next_action(self, module: str, stage: str, thread_type: str = "module") -> str:
        """Get next action based on module, stage, and thread type"""

        # Thread-specific actions
        if thread_type == "company":
            return "setup_company_profile"
        elif thread_type == "product":
            return "setup_product"
        elif thread_type == "service":
            return "setup_service"

        # Module-specific actions (for module thread type)
        action_map = {
            "home": {
                "onboarded": "complete_company_profile",
                "company_profile_completed": "add_products_services",
                "products_added": "integrate_channels",
                "channels_integrated": "explore_other_modules",
            },
            "social": {"default": "setup_social_accounts"},
            "analytics": {"default": "configure_analytics"},
        }

        module_actions = action_map.get(module, {})
        return module_actions.get(stage, module_actions.get("default", "continue_setup"))

    # Legacy methods for backward compatibility
    def create_module_session(self, user_id: str, company_id: str, module: str) -> Dict[str, Any]:
        """Legacy method - use create_session instead"""
        return self.create_session(user_id, company_id, module, "module")

    def create_company_session(self, user_id: str, company_id: str, module: str) -> Dict[str, Any]:
        """Legacy method - use create_session instead"""
        return self.create_session(user_id, company_id, module, "company")

    def create_product_session(self, user_id: str, company_id: str, module: str, product_id: str) -> Dict[str, Any]:
        """Legacy method - use create_session instead"""
        return self.create_session(user_id, company_id, module, "product", product_id)
