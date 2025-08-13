# src\graphs\social_graph.py
from typing import Dict, Any
from langgraph.graph import StateGraph, END
from .base_graph import BaseGraph

class SocialGraph(BaseGraph):
    def __init__(self):
        super().__init__("social")
    
    def _build_graph(self) -> None:
        workflow = StateGraph(dict)
        workflow.add_node("router", self._create_router_node)
        workflow.add_node("process_initial", self._process_initial)
        workflow.add_node("process_user_message", self._process_user_message)
        workflow.add_node("health_check", self._health_check)
        
        workflow.set_entry_point("router")
        workflow.add_conditional_edges("router", lambda x: x, {
            "process_initial": "process_initial",
            "process_user_message": "process_user_message", 
            "health_check": "health_check"
        })
        workflow.add_edge("process_initial", END)
        workflow.add_edge("process_user_message", END)
        workflow.add_edge("health_check", END)
        
        self.graph = workflow.compile()
    
    async def _process_initial(self, state: Dict[str, Any]) -> Dict[str, Any]:
        return {**state, "message": "Hi! I'm your social media assistant. Ready to help with posts, scheduling, and analytics!"}
    
    async def _process_user_message(self, state: Dict[str, Any]) -> Dict[str, Any]:
        return {**state, "message": f"Social: I can help you with that! What specifically do you need?"}
    
    async def _health_check(self, state: Dict[str, Any]) -> Dict[str, Any]:
        return {**state, "message": "Social module healthy", "status": "ok"}