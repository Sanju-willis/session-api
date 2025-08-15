# src\graphs\nodes\router_node.py
from typing import Dict, Any


def router_node(state: Dict[str, Any]) -> Dict[str, Any]:
    """Route based on current stage"""
    stage = state.get("stage")

    next_action_map = {
        "onboarded": "start_onboarding",
        "need_company": "complete_company_profile",
        "company_profile_completed": "add_products_services",
        "products_added": "integrate_channels",
        "channels_integrated": "explore_other_modules",
        "setup_complete": "general_assistance",
    }

    state["next_action"] = next_action_map.get(stage, "continue_setup")
    return state
