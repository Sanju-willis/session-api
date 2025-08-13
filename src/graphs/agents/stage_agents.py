# src\graphs\agents\stage_agents.py
from typing import Dict, Any
from datetime import datetime, timezone

def _now():
    return datetime.now(timezone.utc).isoformat()

class StageAgent:
    async def initial(self, state: Dict[str, Any]) -> Dict[str, Any]:
        raise NotImplementedError

    async def user(self, state: Dict[str, Any]) -> Dict[str, Any]:
        raise NotImplementedError


class DefaultHomeAgent(StageAgent):
    async def initial(self, state: Dict[str, Any]) -> Dict[str, Any]:
        return {**state, "message": "Welcome to home!", "message_type": "assistant", "timestamp": _now()}

    async def user(self, state: Dict[str, Any]) -> Dict[str, Any]:
        return {**state, "message": f"You said: {state.get('user_message','')}", "message_type": "assistant", "timestamp": _now()}


class CreateCompanyAgent(StageAgent):
    async def initial(self, state: Dict[str, Any]) -> Dict[str, Any]:
        # kickoff prompt for create-company stage
        return {
            **state,
            "message": "Let’s set up your company. What’s the company name?",
            "message_type": "assistant",
            "timestamp": _now(),
            "next_action": "ask_company_name",
        }

    async def user(self, state: Dict[str, Any]) -> Dict[str, Any]:
        msg = (state.get("user_message") or "").strip()
        nxt = state.get("context", {}).get("next_action") or state.get("next_action")

        # trivial finite-state example; swap with your own validators/db calls
        if nxt == "ask_company_name":
            if not msg:
                return {**state, "message": "Need a company name.", "message_type": "assistant", "timestamp": _now()}
            # TODO: persist name
            return {
                **state,
                "message": f"Got it: {msg}. What’s the company size?",
                "message_type": "assistant",
                "timestamp": _now(),
                "next_action": "ask_company_size",
                "context": {**state.get("context", {}), "company_name": msg},
            }

        if nxt == "ask_company_size":
            # TODO: validate size, persist, advance stage
            return {
                **state,
                "message": "Saved. Do you want to add products now or skip?",
                "message_type": "assistant",
                "timestamp": _now(),
                "next_action": "ask_add_products",
            }

        return {**state, "message": "Continuing company setup…", "message_type": "assistant", "timestamp": _now()}
