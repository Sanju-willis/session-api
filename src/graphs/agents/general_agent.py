# src\graphs\agents\general_agent.py
from langchain.agents import create_openai_functions_agent, AgentExecutor
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from src.config import settings
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

@tool
def navigate_to_module(module_name: str) -> str:
    """Help users navigate to specific platform modules"""
    return f"To access {module_name}, you can find it in your dashboard navigation menu."

GENERAL_PROMPT = ChatPromptTemplate.from_messages([
    ("system", """You are a helpful assistant for the Kordor platform. The user has completed their initial setup.

YOUR CAPABILITIES:
- Help with general business questions
- Provide guidance on Kordor platform features
- Access user and company information when needed
- Direct users to specific modules
- Answer questions about their setup

TOOLS AVAILABLE:
- get_user_info: Get user details and status
- get_company_info: Get company setup information
- help_with_features: Explain platform features
- navigate_to_module: Help with navigation

APPROACH:
- Be conversational and friendly
- Use tools when you need specific information
- Provide helpful guidance
- Direct users to appropriate modules when needed
- Answer questions based on their completed setup

You can help with any questions about their business, the platform, or general assistance."""),
    ("human", "{input}"),
    ("placeholder", "{agent_scratchpad}"),
])

def get_general_agent():
    llm = ChatOpenAI(
        openai_api_key=settings.OPENAI_API_KEY,
        model="gpt-4",
        temperature=0.7,
    )

    tools = [
        get_user_info,
        get_company_info,
        help_with_features,
        navigate_to_module,
    ]

    agent = create_openai_functions_agent(llm, tools, GENERAL_PROMPT)
    
    return AgentExecutor(
        agent=agent,
        tools=tools,
        verbose=True,
        return_intermediate_steps=True,
        max_iterations=3,
        handle_parsing_errors=True
    )