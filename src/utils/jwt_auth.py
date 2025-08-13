# src\utils\jwt_auth.py
from fastapi import Depends, HTTPException, status, Request
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from src.core.db import get_db
from pydantic import BaseModel
from src.config.settings import settings

SECRET_KEY = settings.JWT_SECRET
ALGORITHM = settings.JWT_ALGORITHM
COOKIE_NAME = "token"


class ReqContext(BaseModel):
    user_id: str
    company_id: str


def get_user_context(request: Request, db: Session = Depends(get_db)) -> ReqContext:
    # Get token from cookie
    token = request.cookies.get(COOKIE_NAME)
    if not token:
        raise HTTPException(status_code=401, detail="Token not found")

    # Decode token
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

    # Extract user_id and company_id
    user_id = payload.get("userId")
    company_id = payload.get("companyId")

    if not user_id:
        raise HTTPException(status_code=401, detail="Invalid user ID in token")

    if not company_id:
        raise HTTPException(status_code=401, detail="Invalid company ID in token")

    return ReqContext(user_id=user_id, company_id=company_id)
