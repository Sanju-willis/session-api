# src\controllers\chat_controller.py
from sqlalchemy.orm import Session as OrmSession
from src.schemas import SendMessageIn, MessageOut
from src.services import process_agent_message
from datetime import datetime

async def send_message_ctrl(payload: SendMessageIn, db: OrmSession) -> MessageOut:
    response_data = await process_agent_message(
        session_id=payload.session_id, 
        message=payload.message, 
        module=payload.message_type
    )
    print(f"Response data: {response_data}")
    
    return MessageOut(
        message=response_data["message"],
        message_type=response_data.get("message_type"),
        timestamp=datetime.now().isoformat(),
        session_id=payload.session_id,
        stage=response_data.get("stage", "response"),
        node=response_data.get("node", "unknown"),
    )