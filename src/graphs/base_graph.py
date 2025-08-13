# src\graphs\base_graph.py
from abc import ABC, abstractmethod
from typing import Dict, Any
from langgraph.graph import StateGraph, END
from datetime import datetime, timezone

def _now():
    return datetime.now(timezone.utc).isoformat()

class BaseGraph(ABC):
    def __init__(self, name: str):
        self.name = name
        self.graph = None
        self._build_graph()

    def _build_graph(self) -> None:
        wf = StateGraph(dict)
        wf.add_node("router", self._create_router_node)
        wf.add_node("process_initial", self._process_initial)
        wf.add_node("process_user_message", self._process_user_message)
        wf.set_entry_point("router")
        wf.add_conditional_edges(
            "router",
            lambda s: s["route"],
            {
                "process_initial": "process_initial",
                "process_user_message": "process_user_message",
            },
        )
        wf.add_edge("process_initial", END)
        wf.add_edge("process_user_message", END)
        self.graph = wf.compile()

    def _create_router_node(self, state: Dict[str, Any]) -> Dict[str, Any]:
        return {
            **state,
            "route": "process_initial" if state.get("message_type") == "initial" else "process_user_message",
        }

    def _append_message(self, state: Dict[str, Any], role: str, content: str) -> Dict[str, Any]:
        """Add a message entry into state['messages'] and return updated state."""
        messages = state.get("messages", [])
        messages.append({
            "role": role,
            "content": content,
            "timestamp": _now(),
        })
        
        # Clean state - only keep essential fields, no nested context
        return {
            "user_id": state.get("user_id"),
            "company_id": state.get("company_id"), 
            "module": state.get("module"),
            "stage": state.get("stage"),
            "step": state.get("step", 1),
            "messages": messages,
            "next_action": state.get("next_action", ""),
        }

    @abstractmethod
    async def _process_initial(self, state: Dict[str, Any]) -> Dict[str, Any]:
        ...

    @abstractmethod
    async def _process_user_message(self, state: Dict[str, Any]) -> Dict[str, Any]:
        ...

    async def invoke(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        result = await self.graph.ainvoke(input_data)
        
        # Auto-save state after processing
        session_id = input_data.get("session_id")
        if session_id and result:
            await self._save_state(session_id, result)
        
        return result
    
    async def _save_state(self, session_id: str, state: Dict[str, Any]) -> None:
        """Save clean state back to persistence layer"""
        try:
            from src.services.langraph_service import LangGraphService
            service = LangGraphService()
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
            
            with service.manager.get_app() as app:
                app.update_state(config, clean_state)
        except Exception as e:
            # Log error but don't break the response
            print(f"Failed to save state: {e}")