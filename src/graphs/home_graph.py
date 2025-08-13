# src\graphs\home_graph.py
from typing import Dict, Any
from .base_graph import BaseGraph

class HomeGraph(BaseGraph):
    def __init__(self):
        super().__init__("home")

    async def _process_initial(self, state: Dict[str, Any]) -> Dict[str, Any]:
        msg = "Welcome to home!"
        clean_state = self._append_message(state, "assistant", msg)
        clean_state["message"] = msg
        clean_state["message_type"] = "assistant"
        return clean_state

    async def _process_user_message(self, state: Dict[str, Any]) -> Dict[str, Any]:
        msg = f"You said: {state.get('user_message', '')}"
        clean_state = self._append_message(state, "assistant", msg)
        clean_state["message"] = msg
        clean_state["message_type"] = "assistant"
        return clean_state