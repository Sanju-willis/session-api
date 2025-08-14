# src\routers\agent_router.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session as OrmSession
from src.core.db import get_db
from src.utils.jwt_auth import get_user_context, ReqContext
from src.schemas.session_schema import StartSessionRequest, SessionResponse
from src.controllers import session_ctrl


router = APIRouter(prefix="/chat", tags=["agent-sessions"])


@router.post("/session", response_model=SessionResponse)
async def start_session(
    request: StartSessionRequest,
    user_ctx: ReqContext = Depends(get_user_context),
    db: OrmSession = Depends(get_db),
):
    return await session_ctrl(request, user_ctx, db)
