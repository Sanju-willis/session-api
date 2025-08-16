# src\controllers\chat_controller.py
from sqlalchemy.orm import Session as OrmSession
from src.schemas import SendMessageIn, MessageOut
from src.services import process_agent_message
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


async def send_message_ctrl(payload: SendMessageIn, db: OrmSession):
    try:
        response = await process_agent_message(payload.session_id, payload.message)

        # Extract AI message content
        ai_message = "No response generated"
        node_name = "unknown"

        if response and response.get("messages"):
            messages = response["messages"]
            if messages:
                last_message = messages[-1]
                if hasattr(last_message, "content"):
                    ai_message = last_message.content
                if hasattr(last_message, "name") and last_message.name:
                    node_name = last_message.name.replace("_agent", "")

        return MessageOut(
            message=ai_message,
            message_type="text",
            timestamp=datetime.now().isoformat(),
            session_id=payload.session_id,
            stage=response.get("stage", "unknown"),
            node=node_name,
        )

    except Exception as e:
        logger.error(f"Chat error: {e}")
        return MessageOut(
            message="Something went wrong. Please try again.",
            message_type="error",
            timestamp=datetime.now().isoformat(),
            session_id=payload.session_id,
            stage="error",
            node="controller",
        )
