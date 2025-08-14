# src\routers\agent_router.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session as OrmSession
from src.core.db import get_db
from src.utils.jwt_auth import get_user_context, ReqContext
from src.schemas.session_schema import StartSessionRequest, SessionResponse
from src.controllers.agent_controller import (
    session_ctrl,
    module_session_ctrl,
    company_session_ctrl,
    product_session_ctrl,
)

router = APIRouter(prefix="/chat", tags=["agent-sessions"])

# NEW UNIFIED ROUTE
@router.post("/session", response_model=SessionResponse)
async def start_session(
    request: StartSessionRequest,
    user_ctx: ReqContext = Depends(get_user_context),
    db: OrmSession = Depends(get_db),
):
    """
    Unified session endpoint - handles all thread types
    Frontend sends: {module: "home", thread_type: "company", item_id: "product123"}
    """
    return await session_ctrl(request, user_ctx, db)

# NEW UNIFIED ROUTE WITH ITEM_ID IN URL
@router.post("/session/{item_id}", response_model=SessionResponse)
async def start_session_with_item(
    item_id: str,
    request: StartSessionRequest,
    user_ctx: ReqContext = Depends(get_user_context),
    db: OrmSession = Depends(get_db),
):
    """
    Unified session endpoint with item_id in URL
    Frontend sends: {module: "home", thread_type: "product"}
    """
    return await session_ctrl(request, user_ctx, db, item_id)

# LEGACY ROUTES (for backward compatibility)
@router.post("/start-session", response_model=SessionResponse)
async def module_session(
    request: StartSessionRequest,
    user_ctx: ReqContext = Depends(get_user_context),
    db: OrmSession = Depends(get_db),
):
    """Legacy module session endpoint"""
    return await module_session_ctrl(request, user_ctx, db)

@router.post("/start-company-session", response_model=SessionResponse)
async def company_session(
    request: StartSessionRequest,
    user_ctx: ReqContext = Depends(get_user_context),
    db: OrmSession = Depends(get_db),
):
    """Legacy company session endpoint"""
    return await company_session_ctrl(request, user_ctx, db)

@router.post("/start-product-session", response_model=SessionResponse)
async def start_product_session(
    request: StartSessionRequest,
    user_ctx: ReqContext = Depends(get_user_context),
    db: OrmSession = Depends(get_db),
):
    """Legacy product session endpoint"""
    product_id = request.productId
    if not product_id:
        raise HTTPException(status_code=400, detail="productId is required")
    
    return await product_session_ctrl(request, user_ctx, db, product_id)