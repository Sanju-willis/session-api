# src\services\agent_responder.py
from typing import Dict, Any, Optional
from src.services.langraph_service import LangGraphService
from src.graphs import HomeGraph, SocialGraph, AnalyticsGraph
from src.types_.thread_types import Module
from src.utils.logging import setup_logging

logger = setup_logging(__name__)

DEFAULT_MESSAGE = "Hello! How can I assist you today?"


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
            logger.warning(f"Unknown module: {module}, defaulting to HOME")
            return self._graphs[Module.HOME]


# Global router
agent_router = AgentRouter()


async def generate_agent_reply(session_id: str, module: Optional[str] = None) -> str:
    try:
        state = await _get_session_state(session_id)
        if not state:
            return DEFAULT_MESSAGE

        module = state.get("module", module)
        graph = agent_router.get_graph(module)

        response = await graph.invoke(
            {
                "session_id": session_id,
                "message_type": "initial",
                "module": module,
                "stage": state.get("stage", "initial"),
                "next_action": state.get("next_action", ""),
                "user_id": state.get("user_id"),
                "company_id": state.get("company_id"),
                "messages": state.get("messages", []),
            }
        )

        # Save updated state
        # Note: State auto-saves in BaseGraph.invoke()
        return response.get("message", DEFAULT_MESSAGE)
    except Exception as e:
        logger.error(f"Error generating initial reply for session {session_id}: {e}")
        return DEFAULT_MESSAGE


async def process_agent_message(session_id: str, message: str, module: Optional[str] = None) -> str:
    try:
        state = await _get_session_state(session_id)
        if not state:
            return "I couldn't find your session. Please try again."

        module = state.get("module", module)
        graph = agent_router.get_graph(module)

        response = await graph.invoke(
            {
                "session_id": session_id,
                "user_message": message,
                "module": module,
                "stage": state.get("stage", "initial"),
                "next_action": state.get("next_action", ""),
                "user_id": state.get("user_id"),
                "company_id": state.get("company_id"),
                "messages": state.get("messages", []),
            }
        )

        # Save updated state
        # Note: State auto-saves in BaseGraph.invoke()
        return response.get("message", "I'm processing your request...")
    except Exception as e:
        logger.error(f"Error processing message for session {session_id}: {e}")
        return "I'm sorry, I encountered an error. Please try again."


async def _get_session_state(session_id: str) -> Optional[Dict[str, Any]]:
    try:
        service = LangGraphService()
        config = {"configurable": {"thread_id": session_id}}
        with service.manager.get_app() as app:
            current_state = app.get_state(config)
            print(f"Retrieved state for session {session_id}: {current_state}")

        if current_state and current_state.values:
            vals = current_state.values
            return {
                "module": vals.get("module"),
                "stage": vals.get("stage"),
                "step": vals.get("step"),
                "user_id": vals.get("user_id"),
                "company_id": vals.get("company_id"),
                "context": vals.get("context", {}),
                "messages": vals.get("messages", []),
                "next_action": vals.get("next_action", ""),
            }
        return None
    except Exception as e:
        logger.warning(f"Could not retrieve state for session {session_id}: {e}")
        return None
