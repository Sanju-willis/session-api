# src\schemas\jwt_schema.py
from pydantic import BaseModel

class UserContext(BaseModel):
    user_id: str  # Changed from userId
    company_id: str  #
