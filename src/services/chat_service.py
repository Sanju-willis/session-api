# src\services\chat_service.py
from src.graphs import HomeGraph, SocialGraph, AnalyticsGraph
from src.types_ import Module
from src.utils import get_session_state, log_error, update_partial_state
from langchain_core.messages import HumanMessage
from typing import Dict, Any


class AgentRouter:
    def __init__(self):
        self._graphs = {
            Module.HOME: HomeGraph(),
            Module.SOCIAL: SocialGraph(),
            Module.ANALYTICS: AnalyticsGraph(),
        }

    def get_graph(self, module: str):
        try:
            return self._graphs[Module(module)]
        except (ValueError, KeyError):
            log_error(f"Unknown module: {module}, defaulting to HOME")
            return self._graphs[Module.HOME]


# Global router
agent_router = AgentRouter()


async def process_agent_message(session_id: str, message: str) -> Dict[str, Any]:
    try:
        # Get session state
        state = get_session_state(session_id)
        if not state:
            log_error(f"No session found for ID: {session_id}")
            return _error_response("Session not found")

        # Get graph and prepare messages
        graph = agent_router.get_graph(state.get("module"))
        messages = state.get("messages", [])
        messages.append(HumanMessage(content=message))

        # Invoke graph
        response = await graph.invoke(
            {
                "session_id": session_id,
                "user_message": message,
                "module": state.get("module"),
                "stage": state.get("stage"),
                "next_action": state.get("next_action", ""),
                "user_id": state.get("user_id"),
                "company_id": state.get("company_id"),
                "messages": messages,
            }
        )

        # Update session state
        update_partial_state(session_id, response)

        return response

    except Exception as e:
        log_error(f"Error processing message for session {session_id}: {e}")
        return _error_response("Processing error occurred")


def _error_response(error_msg: str) -> Dict[str, Any]:
    """Create standardized error response"""
    return {"messages": [], "stage": "error", "next_action": "retry", "error": error_msg}
