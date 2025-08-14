# src\graphs\agents\company_agent.py
from langchain.tools import tool
from langgraph.prebuilt import create_react_agent
from langchain_openai import ChatOpenAI
from src.config.settings import settings

@tool
def fill_company_profile() -> str:
    """Start onboarding by collecting company details."""
    return "Please share your company name, size, and industry."

@tool
def collect_company_info() -> str:
    """Collect specific company information step by step."""
    return "Let me help you complete your company profile. What's your company name?"

def get_company_agent():
    llm = ChatOpenAI(
        openai_api_key=settings.OPENAI_API_KEY,
        model="gpt-4",
        temperature=0,
    )
    
    # ✅ Remove state_modifier - not supported by create_react_agent
    return create_react_agent(llm, [fill_company_profile, collect_company_info])