# src\services\thread_manager.py
from src.types_ import Module, ThreadInfo, ThreadType
from src.utils import generate_thread_id


class ThreadManager:
    def __init__(self):
        self.active_threads = {}

    def get_thread(
        self, user_id: str, company_id: str, module: str, thread_type: str, entity_id: str, item_id: str = None
    ) -> ThreadInfo:
        # Convert strings to enums
        module_enum = Module(module)
        thread_type_enum = ThreadType(thread_type)

        # Generate thread ID
        # print(f"Generating thread ID for user: item: {entity_id}", {thread_type_enum})
        thread_id = generate_thread_id(user_id, company_id, module_enum, thread_type_enum, item_id, entity_id)

        # Check if thread already exists
        if thread_id in self.active_threads:
            return self.active_threads[thread_id]

        # Set parent thread for sub-threads
        parent_thread_id = None
        if thread_type in ["company", "product", "service"]:
            parent_thread_id = generate_thread_id(user_id, company_id, module_enum, ThreadType.MODULE)

        # Determine initial stage

        # Create thread info
        thread_info = ThreadInfo(
            thread_id=thread_id,
            parent_thread_id=parent_thread_id,
        )

        # Cache the thread
        self.active_threads[thread_id] = thread_info

        return thread_info
