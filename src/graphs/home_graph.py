# src\graphs\home_graph.py
from langgraph.graph import StateGraph, END
from typing import Dict, Any
from .nodes import company_node, product_node, router_node, onboarding_node, general_node
from src.utils import update_partial_state


class HomeGraph:
    def __init__(self):
        self.name = "home"
        self.graph = self._build()

    def _build(self):
        wf = StateGraph(dict)

        # Nodes - imported from separate files
        wf.add_node("router", router_node)
        wf.add_node("onboarding", onboarding_node)
        wf.add_node("company_agent", company_node)
        wf.add_node("product_agent", product_node)
        wf.add_node("general", general_node)

        # Entry
        wf.set_entry_point("router")

        # Conditional routing
        wf.add_conditional_edges(
            "router",
            lambda state: state.get("stage"),
            {
                "onboarded": "onboarding",
                "need_company": "company_agent",
                "company_profile_completed": "product_agent",
                "setup_complete": "general",
            },
        )

        # Endpoints
        wf.add_edge("onboarding", END)
        wf.add_edge("company_agent", END)
        wf.add_edge("product_agent", END)
        wf.add_edge("general", END) 

        return wf.compile()

    async def invoke(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        result = await self.graph.ainvoke(input_data)

        # Update session state if session_id exists
        session_id = input_data.get("session_id")
        if session_id and result:
            update_partial_state(session_id, result)

        return result
