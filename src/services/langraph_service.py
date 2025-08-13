# src\services\langraph_service.py
from src.services.thread_manager import ThreadManager, Module, HomeStage
from src.core.langraph_config import LangGraphManager
from src.types_.conversation_type import ConversationState
from typing import Dict, Any


class LangGraphService:
    def __init__(self):
        self.manager = LangGraphManager()
        self.thread_manager = ThreadManager()

    def create_module_session(self, user_id: str, company_id: str, module: str) -> Dict[str, Any]:
        module_enum = Module(module.lower())
        thread_info = self.thread_manager.get_module_thread(user_id, company_id, module_enum)

        initial_state = self._build_initial_state(user_id, company_id, module, thread_info.stage)

        self._persist_state(thread_info.thread_id, initial_state)

        return {
            "session_id": thread_info.thread_id,
            "module": module,
            "thread_type": "module",
            "stage": thread_info.stage,
            "next_action": self._get_next_action(module_enum, thread_info.stage),
        }

    def create_company_session(self, user_id: str, company_id: str) -> Dict[str, Any]:
        thread_info = self.thread_manager.get_company_thread(user_id, company_id)

        initial_state = self._build_initial_state(
            user_id, company_id, "home", "initial", context={"sub_module": "company_profile"}
        )

        self._persist_state(thread_info.thread_id, initial_state)

        return {
            "session_id": thread_info.thread_id,
            "thread_type": "company",
            "module": "home",
            "stage": "initial",
            "next_action": "setup_company_profile",
            "parent_thread": thread_info.parent_thread_id,
        }

    def create_product_session(self, user_id: str, company_id: str, product_id: str) -> Dict[str, Any]:
        thread_info = self.thread_manager.get_product_thread(user_id, company_id, product_id)

        initial_state = self._build_initial_state(
            user_id, company_id, "home", "initial", context={"sub_module": "product", "product_id": product_id}
        )

        self._persist_state(thread_info.thread_id, initial_state)

        return {
            "session_id": thread_info.thread_id,
            "thread_type": "product",
            "module": "home",
            "product_id": product_id,
            "stage": "initial",
            "next_action": "setup_product",
            "parent_thread": thread_info.parent_thread_id,
        }

    def _build_initial_state(
        self, user_id: str, company_id: str, module: str, stage: str, context: Dict[str, Any] = None
    ) -> ConversationState:
        """Build initial conversation state"""
        return ConversationState(
            user_id=user_id,
            company_id=company_id,
            module=module,
            messages=[],
            stage=stage,
            step=1,
            context=context or {},
        )

    def _persist_state(self, thread_id: str, state: ConversationState) -> None:
        """Persist state to LangGraph"""
        config = {"configurable": {"thread_id": thread_id}}
        with self.manager.get_app() as app:
            app.invoke(state, config=config)

    def _get_next_action(self, module: Module, stage: str) -> str:
        """Determine next action based on module and stage"""
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
