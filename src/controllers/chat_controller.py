# src\controllers\chat_controller.py
from sqlalchemy.orm import Session as OrmSession
from src.schemas import SendMessageIn, MessageOut
from src.services import process_agent_message
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


async def send_message_ctrl(payload: SendMessageIn, db: OrmSession) -> MessageOut:
    try:
        response_data = await process_agent_message(
            session_id=payload.session_id,
            message=payload.message,
        )

        # Handle string response
        if isinstance(response_data, str):
            response_data = {"message": response_data}

        return MessageOut(
            message=response_data.get("message", "Error occurred"),
            message_type=response_data.get("message_type", "text"),
            timestamp=datetime.now().isoformat(),
            session_id=payload.session_id,
            stage=response_data.get("stage", "response"),
            node=response_data.get("node", "unknown"),
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
