# src\dependencies\shared.py
# src/dependencies/shared.py
from fastapi import Depends
from src.core.db import get_db
from src.utils.jwt_auth import get_user_context, ReqContext
from sqlalchemy.orm import Session

class RequestCtx:
    def __init__(self, user: ReqContext, db: Session):
        self.user = user
        self.db = db

def get_request_ctx(
    user: ReqContext = Depends(get_user_context),
    db: Session = Depends(get_db)
) -> RequestCtx:
    return RequestCtx(user, db)
