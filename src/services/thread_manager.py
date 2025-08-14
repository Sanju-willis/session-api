# src\services\thread_manager.py
from src.types_.thread_types import Module, ThreadInfo, HomeStage, ThreadType
from src.utils import generate_thread_id


class ThreadManager:
    def __init__(self):
        self.active_threads = {}

    def get_thread(
        self, user_id: str, company_id: str, module: str, thread_type: str, item_id: str = None
    ) -> ThreadInfo:
        """Unified method to get any thread type"""

        # Convert strings to enums
        module_enum = Module(module)
        thread_type_enum = ThreadType(thread_type)

        # Generate thread ID
        thread_id = generate_thread_id(user_id, company_id, module_enum, thread_type_enum, item_id)

        # Check if thread already exists
        if thread_id in self.active_threads:
            return self.active_threads[thread_id]

        # Set parent thread for sub-threads
        parent_thread_id = None
        if thread_type in ["company", "product", "service"]:
            parent_thread_id = generate_thread_id(user_id, company_id, module_enum, ThreadType.MODULE)

        # Determine initial stage
        initial_stage = self._get_initial_stage(module_enum, thread_type_enum)

        # Build metadata
        metadata = self._build_metadata(user_id, company_id, module, item_id, thread_type)

        # Create thread info
        thread_info = ThreadInfo(
            thread_id=thread_id,
            thread_type=thread_type_enum,
            module=module_enum,
            parent_thread_id=parent_thread_id,
            item_id=item_id,
            stage=initial_stage,
            metadata=metadata,
        )

        # Cache the thread
        self.active_threads[thread_id] = thread_info

        return thread_info

    def _get_initial_stage(self, module: Module, thread_type: ThreadType) -> str:
        """Determine initial stage based on module and thread type"""
        if thread_type == ThreadType.MODULE and module == Module.HOME:
            return HomeStage.ONBOARDED.value
        else:
            return "initial"

    def _build_metadata(
        self, user_id: str, company_id: str, module: str, item_id: str = None, thread_type: str = "module"
    ) -> dict:
        """Build metadata dictionary based on thread type"""
        metadata = {
            "user_id": user_id,
            "company_id": company_id,
            "module": module,
            "thread_type": thread_type,
        }

        if item_id:
            if thread_type == "product":
                metadata["product_id"] = item_id
            elif thread_type == "service":
                metadata["service_id"] = item_id
            else:
                metadata["item_id"] = item_id

        return metadata
