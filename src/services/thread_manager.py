# src\services\thread_manager.py
from src.types_ import Module, ThreadInfo, ThreadType
from src.utils import generate_thread_id
from typing import Optional
from pprint import pprint

class ThreadManager:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.active_threads = {}
        return cls._instance

    def get_thread(
        self, user_id: str, company_id: str, module: Module, thread_type: ThreadType, 
        entity_id: str,  parent_thread_id: Optional[str] = None
    ) -> ThreadInfo:
        
        thread_id = generate_thread_id(user_id, company_id, module, thread_type, entity_id)
        
        
        # Check if thread already exists
        if thread_id in self.active_threads:
            pprint("Found existing thread")
            return self.active_threads[thread_id]
        
        # Validate parent thread for sub-threads
        if thread_type.value in ["company", "product", "service"]:
            if parent_thread_id is None:
                raise ValueError(f"parent_thread_id required for thread_type: {thread_type.value}")

            if parent_thread_id not in self.active_threads:
                raise ValueError(f"Parent thread {parent_thread_id} not found")
        
        # Create thread info
        thread_info = ThreadInfo(
            thread_id=thread_id,
            parent_thread_id=parent_thread_id,
        )
        
        # Cache the thread
        self.active_threads[thread_id] = thread_info
        
        return thread_info