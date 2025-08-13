# src\controllers\sessions_controller.py
from sqlalchemy.orm import Session as OrmSession
from src.schemas import SendMessageIn, MessageOut
from src.services.agent_responder import process_agent_message
from datetime import datetime


async def send_message_ctrl(payload: SendMessageIn, db: OrmSession) -> MessageOut:
    response_message = await process_agent_message(
        session_id=payload.session_id,
        message=payload.message,
        module=payload.message_type
    )
    
    return MessageOut(
    message=response_message,
    message_type="assistant",
    timestamp=datetime.now().isoformat()
)