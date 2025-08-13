# src\graphs\home_graphy.py
from typing import Dict, Any
from langgraph.graph import StateGraph, END
from src.utils import update_partial_state, append_message


class HomeGraph:
    def __init__(self):
        self.name = "home"
        self.graph = self._build_graph()

    def _build_graph(self):
        wf = StateGraph(dict)

        # Define nodes
        wf.add_node("router", self._router)
        wf.add_node("company_agent", self._company_agent)
        wf.add_node("product_agent", self._product_agent)

        # Entry point
        wf.set_entry_point("router")

        # Routing logic based on stage
        wf.add_conditional_edges(
            "router",
            lambda s: s.get("stage"),
            {
                "onboarded": "company_agent",
                "company_profile_completed": "product_agent",
            },
        )

        wf.add_edge("company_agent", END)
        wf.add_edge("product_agent", END)

        return wf.compile()

    def _router(self, state: Dict[str, Any]) -> Dict[str, Any]:
        return state  # Pass state directly; routing uses lambda above

    async def _company_agent(self, state: Dict[str, Any]) -> Dict[str, Any]:
        msg = "Let's fill in your company profile!"
        clean_state = append_message(state, "assistant", msg)
        clean_state["message"] = msg
        clean_state["message_type"] = "assistant"
        return clean_state

    async def _product_agent(self, state: Dict[str, Any]) -> Dict[str, Any]:
        msg = "Now let's add your products or services!"
        clean_state = append_message(state, "assistant", msg)
        clean_state["message"] = msg
        clean_state["message_type"] = "assistant"
        return clean_state

    async def invoke(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        result = await self.graph.ainvoke(input_data)

        session_id = input_data.get("session_id")
        if session_id and result:
            update_partial_state(session_id, result)

        return result
