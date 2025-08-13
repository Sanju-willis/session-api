# src\services\thread_manager.py
import hashlib
from typing import Optional
from src.types_.thread_types import Module, ThreadInfo, HomeStage, ThreadType


class ThreadManager:
    def __init__(self):
        self.active_threads = {}

    def generate_thread_id(
        self,
        user_id: str,
        company_id: str,
        module: Module,
        thread_type: ThreadType = ThreadType.MODULE,
        item_id: Optional[str] = None,
    ) -> str:
        """Generate thread ID based on module, type and context"""
        if thread_type == ThreadType.MODULE:
            key = f"{user_id}:{company_id}:{module.value}"

        elif thread_type == ThreadType.COMPANY:
            key = f"{user_id}:{company_id}:{module.value}:company"
        elif thread_type == ThreadType.PRODUCT:
            key = f"{user_id}:{company_id}:{module.value}:product:{item_id}"
        elif thread_type == ThreadType.CHANNEL:
            key = f"{user_id}:{company_id}:{module.value}:channel:{item_id}"

        return hashlib.md5(key.encode()).hexdigest()

    def get_module_thread(self, user_id: str, company_id: str, module: Module) -> ThreadInfo:
        thread_id = self.generate_thread_id(user_id, company_id, module, ThreadType.MODULE)

        if thread_id in self.active_threads:
            return self.active_threads[thread_id]

        if module == Module.HOME:
            initial_stage = HomeStage.ONBOARDED.value
        else:
            initial_stage = "initial"

        return ThreadInfo(
            thread_id=thread_id,
            thread_type=ThreadType.MODULE,
            module=module,
            parent_thread_id=None,
            item_id=None,
            stage=initial_stage,
            metadata={
                "user_id": user_id,
                "company_id": company_id,
                "module": module.value,
            },
        )

    def get_company_thread(self, user_id: str, company_id: str) -> ThreadInfo:
        home_thread_id = self.generate_thread_id(user_id, company_id, Module.HOME, ThreadType.MODULE)
        thread_id = self.generate_thread_id(user_id, company_id, Module.HOME, ThreadType.COMPANY)

        return ThreadInfo(
            thread_id=thread_id,
            thread_type=ThreadType.COMPANY,
            module=Module.HOME,
            parent_thread_id=home_thread_id,
            item_id=None,
            stage="initial",
            metadata={"user_id": user_id, "company_id": company_id},
        )

    def get_product_thread(self, user_id: str, company_id: str, product_id: str) -> ThreadInfo:
        """Get individual product thread (under home module)"""
        home_thread_id = self.generate_thread_id(user_id, company_id, Module.HOME, ThreadType.MODULE)
        thread_id = self.generate_thread_id(user_id, company_id, Module.HOME, ThreadType.PRODUCT, product_id)

        return ThreadInfo(
            thread_id=thread_id,
            thread_type=ThreadType.PRODUCT,
            module=Module.HOME,
            parent_thread_id=home_thread_id,
            item_id=product_id,
            stage="initial",
            metadata={
                "user_id": user_id,
                "company_id": company_id,
                "product_id": product_id,
            },
        )
