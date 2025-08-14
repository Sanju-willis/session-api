# src\routers\agent_router.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session as OrmSession
from src.core.db import get_db
from src.utils.jwt_auth import get_user_context, ReqContext
from src.schemas.session_schema import StartSessionRequest, SessionResponse
from src.controllers.agent_controller import (
    module_session_ctrl,
    company_session_ctrl,
    product_session_ctrl,
)

router = APIRouter(prefix="/chat", tags=["agent-sessions"])


@router.post("/start-session", response_model=SessionResponse)
async def module_session(
    request: StartSessionRequest,
    user_ctx: ReqContext = Depends(get_user_context),
    db: OrmSession = Depends(get_db),
):
    return await module_session_ctrl(request, user_ctx, db)


@router.post("/start-company-session", response_model=SessionResponse)
async def company_session(
    request: StartSessionRequest, user_ctx: ReqContext = Depends(get_user_context), db: OrmSession = Depends(get_db)
):
    return await company_session_ctrl(request, user_ctx, db)


@router.post("/start-product-session", response_model=SessionResponse)
async def start_product_session(
    request: StartSessionRequest,
    user_ctx: ReqContext = Depends(get_user_context),
    db: OrmSession = Depends(get_db),
):
    product_id = request.productId
    if not product_id:
        raise HTTPException(status_code=400, detail="productId is required")

    return await product_session_ctrl(request, user_ctx, db, product_id)