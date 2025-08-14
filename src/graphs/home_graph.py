# src\graphs\home_graph.py
from langgraph.graph import StateGraph, END
from typing import Dict, Any
from .agents import get_company_agent, get_product_agent
from src.utils import update_partial_state, append_message


class HomeGraph:
    def __init__(self):
        self.name = "home"
        self.graph = self._build()

    def _build(self):
        wf = StateGraph(dict)

        # Nodes
        wf.add_node("router", self._router_node)
        wf.add_node("company_agent", self._company_node)
        wf.add_node("product_agent", self._product_node)

        # Entry
        wf.set_entry_point("router")

        # Conditional routing
        wf.add_conditional_edges(
            "router",
            lambda state: state.get("stage"),
            {"onboarded": "company_agent", "company_profile_completed": "product_agent"},
        )

        # Endpoints
        wf.add_edge("company_agent", END)
        wf.add_edge("product_agent", END)

        return wf.compile()

    def _router_node(self, state: Dict[str, Any]) -> Dict[str, Any]:
        return state

    async def _company_node(self, state: Dict[str, Any]) -> Dict[str, Any]:
        agent = get_company_agent()
        response = await agent.ainvoke({"messages": [("user", "Start company onboarding")]})
        final_message = response["messages"][-1].content

        # Update state with message and append to conversation
        clean_state = append_message(state, "assistant", final_message)
        clean_state["message"] = final_message
        clean_state["message_type"] = "assistant"
        return clean_state

    async def _product_node(self, state: Dict[str, Any]) -> Dict[str, Any]:
        agent = get_product_agent()
        response = await agent.ainvoke({"messages": [("user", "Let's collect product details")]})
        final_message = response["messages"][-1].content

        # Update state with message and append to conversation
        clean_state = append_message(state, "assistant", final_message)
        clean_state["message"] = final_message
        clean_state["message_type"] = "assistant"
        return clean_state

    async def invoke(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        result = await self.graph.ainvoke(input_data)

        # Update session state if session_id exists
        session_id = input_data.get("session_id")
        if session_id and result:
            update_partial_state(session_id, result)

        return result
