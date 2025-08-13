# src\graphs\onboarding_graph.py
from langgraph.graph import StateGraph, END
from typing import Dict, Any
from .agents import get_company_agent, get_product_agent

class OnboardingGraph:
    def __init__(self):
        self.graph = self._build()

    def _build(self):
        wf = StateGraph(dict)

        wf.add_node("router", self._router_node)
        wf.add_node("company_agent", self._company_node)
        wf.add_node("product_agent", self._product_node)

        wf.set_entry_point("router")

        wf.add_conditional_edges(
            "router",
            lambda state: state.get("stage"),
            {
                "onboarded": "company_agent",
                "company_profile_completed": "product_agent"
            }
        )

        wf.add_edge("company_agent", END)
        wf.add_edge("product_agent", END)

        return wf.compile()

    def _router_node(self, state: Dict[str, Any]) -> Dict[str, Any]:
        return state

    async def _company_node(self, state: Dict[str, Any]) -> Dict[str, Any]:
        agent = get_company_agent()
        response = agent.run("Start company onboarding")
        return {**state, "message": response}

    async def _product_node(self, state: Dict[str, Any]) -> Dict[str, Any]:
        agent = get_product_agent()
        response = agent.run("Let's collect product details")
        return {**state, "message": response}

    async def invoke(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        return await self.graph.ainvoke(input_data)
