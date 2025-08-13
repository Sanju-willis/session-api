# src\routers\sessions_router.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session as OrmSession
from src.core.db import get_db
from src.schemas import SendMessageIn, MessageOut
from src.controllers.sessions_controller import send_message_ctrl
from src.utils.logging import setup_logging

logger = setup_logging(__name__)

router = APIRouter(prefix="/sessions", tags=["sessions"])


@router.post("/message", response_model=MessageOut, status_code=200)
async def send_message(payload: SendMessageIn, db: OrmSession = Depends(get_db)):  # Add async
    logger.info(f"Received message: session_id={payload.session_id}, message_type={payload.message_type}")
    logger.debug(f"Full payload: {payload.dict()}")

    result = await send_message_ctrl(payload, db)  # Add await

    logger.info(f"Response generated for session: {payload.session_id}")
    logger.debug(f"Response: {result}")

    return result
