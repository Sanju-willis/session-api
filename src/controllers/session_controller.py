# src\controllers\session_controller.py
from fastapi import HTTPException
from sqlalchemy.orm import Session
from src.utils import ReqContext
from src.services import LangGraphService
from src.schemas import StartSessionRequest, SessionResponse

async def session_ctrl(request: StartSessionRequest, user_ctx: ReqContext, db: Session,  item_id: str = None) -> SessionResponse:
    
    try:
        service = LangGraphService()
        result = service.create_session(
            user_id=user_ctx.user_id,
            company_id=user_ctx.company_id,
            module=request.module,
            thread_type=request.thread_type,
            item_id=request.item_id or item_id,  # Use from request body or URL param
            entity_id=request.entity_id  # Pass entity_id from request body
        )
        
        return SessionResponse(**result)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to start session: {str(e)}")