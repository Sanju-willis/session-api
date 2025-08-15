# src\graphs\agents\general_agent.py
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent
from langchain_core.tools import tool
from typing import Dict, Any

@tool
def get_user_info(user_id: str) -> Dict[str, Any]:
    """Get user information and current status"""
    # Implement user info retrieval logic
    return {"user_id": user_id, "status": "active"}

@tool
def get_company_info(company_id: str) -> Dict[str, Any]:
    """Get company information and setup status"""
    # Implement company info retrieval logic
    return {"company_id": company_id, "setup_complete": True}

@tool
def help_with_features() -> str:
    """Provide help with Kordor platform features"""
    return """
    Kordor platform features:
    - Company Profile Management
    - Product/Service Catalog
    - Channel Integration
    - Analytics and Reporting
    - Customer Management
    """

def get_general_agent():
    """Create and return a general assistance agent"""
    
    # Initialize the LLM
    llm = ChatOpenAI(
        model="gpt-4",
        temperature=0.7,
        streaming=True
    )
    
    # Define available tools
    tools = [
        get_user_info,
        get_company_info,
        help_with_features,
    ]
    
    # Create the agent
    agent = create_react_agent(
        llm,
        tools,
        state_modifier="You are a helpful general assistant for the Kordor platform."
    )
    
    return agent