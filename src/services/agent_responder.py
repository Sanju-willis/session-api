# src\services\agent_responder.py
from typing import Optional
from src.graphs import HomeGraph, SocialGraph, AnalyticsGraph
from src.types_ import Module
from src.utils import setup_logging, get_session_state
from pprint import pprint

logger = setup_logging(__name__)


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


async def process_agent_message(session_id: str, message: str, module: Optional[str] = None) -> str:
    try:
        state = get_session_state(session_id)
        if not state:
            return "I couldn't find your session. Please try again."
        print(f"Processing message for session {session_id}: {state}")

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
        print("🧠 Response from graph:")
        pprint(response, indent=2, width=100)

        return response.get("message", "I'm processing your request...")
    except Exception as e:
        logger.error(f"Error processing message for session {session_id}: {e}")
        return "I'm sorry, I encountered an error. Please try again."
