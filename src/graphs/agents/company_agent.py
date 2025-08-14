# src\graphs\agents\company_agent.py
from langchain.tools import tool
from langgraph.prebuilt import create_react_agent
from langchain_openai import ChatOpenAI
from src.config.settings import settings

@tool
async def fill_company_profile() -> str:
    """Start onboarding by collecting company details."""
    return "Please share your company name, size, and industry."

def get_company_agent():
    llm = ChatOpenAI(
        openai_api_key=settings.OPENAI_API_KEY,
        model="gpt-4",
        temperature=0,
    )
    return create_react_agent(llm, [fill_company_profile])
