# src\graphs\social_graph.py
from typing import Dict, Any
from langgraph.graph import StateGraph, END
from src.utils import update_partial_state, append_message


class SocialGraph:
    def __init__(self):
        self.name = "social"
        self.graph = self._build_graph()

    def _build_graph(self):
        wf = StateGraph(dict)
        wf.add_node("router", self._create_router_node)
        wf.add_node("process_initial", self._process_initial)
        wf.add_node("process_user_message", self._process_user_message)
        wf.add_node("health_check", self._health_check)

        wf.set_entry_point("router")

        wf.add_conditional_edges(
            "router",
            lambda s: s.get("route"),
            {
                "process_initial": "process_initial",
                "process_user_message": "process_user_message",
                "health_check": "health_check",
            },
        )

        wf.add_edge("process_initial", END)
        wf.add_edge("process_user_message", END)
        wf.add_edge("health_check", END)

        return wf.compile()

    def _create_router_node(self, state: Dict[str, Any]) -> Dict[str, Any]:
        message_type = state.get("message_type", "")
        if message_type == "initial":
            route = "process_initial"
        elif message_type == "health":
            route = "health_check"
        else:
            route = "process_user_message"
        return {**state, "route": route}

    async def _process_initial(self, state: Dict[str, Any]) -> Dict[str, Any]:
        msg = "Hi! I'm your social media assistant. Ready to help with posts, scheduling, and analytics!"
        clean_state = append_message(state, "assistant", msg)
        clean_state["message"] = msg
        clean_state["message_type"] = "assistant"
        return clean_state

    async def _process_user_message(self, state: Dict[str, Any]) -> Dict[str, Any]:
        msg = "Social: I can help you with that! What specifically do you need?"
        clean_state = append_message(state, "assistant", msg)
        clean_state["message"] = msg
        clean_state["message_type"] = "assistant"
        return clean_state

    async def _health_check(self, state: Dict[str, Any]) -> Dict[str, Any]:
        msg = "Social module healthy"
        clean_state = append_message(state, "assistant", msg)
        clean_state["message"] = msg
        clean_state["message_type"] = "assistant"
        clean_state["status"] = "ok"
        return clean_state

    async def invoke(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        result = await self.graph.ainvoke(input_data)

        session_id = input_data.get("session_id")
        if session_id and result:
            update_partial_state(session_id, result)

        return result
