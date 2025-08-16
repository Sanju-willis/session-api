# src\graphs\state.py
from langgraph.graph import MessagesState

class CustomState(MessagesState):
    session_id: str = ""
    user_message: str = ""
    module: str = ""
    stage: str = ""
    next_action: str = ""
    user_id: str = ""
    company_id: str = ""