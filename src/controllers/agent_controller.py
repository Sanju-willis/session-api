# src\controllers\agent_controller.py
from fastapi import HTTPException
from sqlalchemy.orm import Session
from src.utils import ReqContext
from src.services import LangGraphService
from src.schemas import StartSessionRequest, SessionResponse


async def module_session_ctrl(request: StartSessionRequest, user_ctx: ReqContext, db: Session) -> SessionResponse:
    """Start module session controller"""
    try:
        service = LangGraphService()
        result = service.create_module_session(
            user_id=user_ctx.user_id,
            company_id=user_ctx.company_id,
            module=request.module,
        )

        return SessionResponse(**result)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to start session: {str(e)}")


async def company_session_ctrl(request: StartSessionRequest, user_ctx: ReqContext, db: Session) -> SessionResponse:
    """Start company session controller"""
    try:
        service = LangGraphService()
        result = service.create_company_session(user_id=user_ctx.user_id, company_id=user_ctx.company_id)

        return SessionResponse(**result)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to start company session: {str(e)}")


async def product_session_ctrl(
    request: StartSessionRequest,
    user_ctx: ReqContext,
    db: Session,
    product_id: str,  # Add product_id parameter
) -> SessionResponse:
    """Start product session controller"""
    try:
        service = LangGraphService()
        result = service.create_product_session(
            user_id=user_ctx.user_id,
            company_id=user_ctx.company_id,
            product_id=product_id,
        )

        return SessionResponse(**result)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to start product session: {str(e)}")
