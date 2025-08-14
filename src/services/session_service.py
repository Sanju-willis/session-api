# src\services\session_service.py
from src.services.thread_manager import ThreadManager, Module, HomeStage
from src.core.langraph_config import LangGraphManager
from typing import Dict, Any
from src.utils import build_initial_state, persist_state


class LangGraphService:
    def __init__(self):
        self.manager = LangGraphManager()
        self.thread_manager = ThreadManager()

    def create_module_session(self, user_id: str, company_id: str, module: str) -> Dict[str, Any]:
        thread_info = self.thread_manager.get_module_thread(user_id, company_id, Module(module))

        initial_state = build_initial_state(user_id, company_id, module, thread_info.stage)

        persist_state(thread_info.thread_id, initial_state)

        return {
            "session_id": thread_info.thread_id,
            "module": module,
            "thread_type": "module",
            "stage": thread_info.stage,
            "next_action": self._get_next_action(Module(module), thread_info.stage),
        }

    def create_company_session(self, user_id: str, company_id: str) -> Dict[str, Any]:
        thread_info = self.thread_manager.get_company_thread(user_id, company_id)

        initial_state = build_initial_state(
            user_id, company_id, "home", "initial", context={"sub_module": "company_profile"}
        )

        persist_state(thread_info.thread_id, initial_state)

        return {
            "session_id": thread_info.thread_id,
            "thread_type": "company",
            "module": "home",
            "stage": "initial",
            "next_action": "setup_company_profile",
            "parent_thread": thread_info.parent_thread_id,
        }

    def create_product_session(self, user_id: str, company_id: str, module: str, product_id: str) -> Dict[str, Any]:
        print(f"Creating product session for user {user_id}, company {company_id}, product {module}")
        thread_info = self.thread_manager.get_product_thread(user_id, company_id, product_id)

        initial_state = build_initial_state(
            user_id, company_id, "home", "initial", context={"sub_module": "product", "product_id": product_id}
        )

        persist_state(thread_info.thread_id, initial_state)

        return {
            "session_id": thread_info.thread_id,
            "thread_type": "product",
            "module": "home",
            "product_id": product_id,
            "stage": "initial",
            "next_action": "setup_product",
            "parent_thread": thread_info.parent_thread_id,
        }

    def _get_next_action(self, module: Module, stage: str) -> str:
        action_map = {
            Module.HOME: {
                HomeStage.ONBOARDED.value: "complete_company_profile",
                HomeStage.COMPANY_PROFILE_COMPLETED.value: "add_products_services",
                HomeStage.PRODUCTS_ADDED.value: "integrate_channels",
                HomeStage.CHANNELS_INTEGRATED.value: "explore_other_modules",
            },
            Module.SOCIAL: {"default": "setup_social_accounts"},
            Module.ANALYTICS: {"default": "configure_analytics"},
        }

        module_actions = action_map.get(module, {})
        return module_actions.get(stage, module_actions.get("default", "continue_setup"))
