# src\graphs\home_graph.py
from langgraph.graph import StateGraph, END
from typing import Dict, Any
from .nodes import company_node, product_node, onboarding_node, general_node
from src.utils import log_state
from .state import CustomState


class HomeGraph:
    def __init__(self):
        self.name = "home"
        self.graph = self._build()

    def _build(self):
        wf = StateGraph(CustomState)

        # Nodes - imported from separate files
        wf.add_node("onboarding", onboarding_node)
        wf.add_node("company_agent", company_node)
        wf.add_node("product_agent", product_node)
        wf.add_node("general", general_node)

        # Direct conditional entry point (no router needed)
        wf.set_conditional_entry_point(
            lambda state: state.get("stage", "setup_complete"),
            {
                "onboarded": "onboarding",
                "need_company": "company_agent",
                "company_completed": "product_agent",
                "setup_complete": "general",
                "__default__": "general",
            },
        )

        # Endpoints
        wf.add_edge("onboarding", END)
        wf.add_edge("company_agent", END)
        wf.add_edge("product_agent", END)
        wf.add_edge("general", END)

        return wf.compile()

    async def invoke(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        # print(f"DEBUG 🏠 HomeGraph: Input data: {input_data}")

        result = await self.graph.ainvoke(input_data)

        if result is None:
            print("ERROR🏠 HomeGraph: Graph returned None!")

        log_state(result)
        return result
