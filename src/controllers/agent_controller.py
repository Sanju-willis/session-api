# src\controllers\agent_controller.py
from fastapi import HTTPException
from sqlalchemy.orm import Session
from src.utils import ReqContext
from src.services import LangGraphService
from src.schemas import StartSessionRequest, SessionResponse

async def session_ctrl(request: StartSessionRequest, user_ctx: ReqContext, db: Session, product_id: str = None) -> SessionResponse:
    """
    Unified session controller - handles all thread types
    Frontend should send: {module: "home", thread_type: "company", item_id: "product123"}
    """
    try:
        service = LangGraphService()
        result = service.create_session(
            user_id=user_ctx.user_id,
            company_id=user_ctx.company_id,
            module=request.module,
            thread_type=request.thread_type,
            item_id=request.item_id or product_id  # Use from request or URL param
        )
        
        return SessionResponse(**result)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to start session: {str(e)}")

# Legacy functions for backward compatibility (hardcode thread_type)
async def module_session_ctrl(request: StartSessionRequest, user_ctx: ReqContext, db: Session) -> SessionResponse:
    """Legacy - hardcode thread_type as 'module'"""
    try:
        service = LangGraphService()
        result = service.create_session(
            user_id=user_ctx.user_id,
            company_id=user_ctx.company_id,
            module=request.module,
            thread_type="module",  # Hardcoded
            item_id=None
        )
        
        return SessionResponse(**result)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to start module session: {str(e)}")

async def company_session_ctrl(request: StartSessionRequest, user_ctx: ReqContext, db: Session) -> SessionResponse:
    """Legacy - hardcode thread_type as 'company'"""
    try:
        service = LangGraphService()
        result = service.create_session(
            user_id=user_ctx.user_id,
            company_id=user_ctx.company_id,
            module=request.module,
            thread_type="company",  # Hardcoded
            item_id=None
        )
        
        return SessionResponse(**result)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to start company session: {str(e)}")

async def product_session_ctrl(request: StartSessionRequest, user_ctx: ReqContext, db: Session, product_id: str) -> SessionResponse:
    """Legacy - hardcode thread_type as 'product'"""
    try:
        service = LangGraphService()
        result = service.create_session(
            user_id=user_ctx.user_id,
            company_id=user_ctx.company_id,
            module=request.module,
            thread_type="product",  # Hardcoded
            item_id=product_id
        )
        
        return SessionResponse(**result)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to start product session: {str(e)}")