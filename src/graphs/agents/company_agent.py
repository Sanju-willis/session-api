# src\graphs\agents\company_agent.py
from src.config.settings import settings
from langchain.agents import initialize_agent, AgentType
from langchain_openai import ChatOpenAI
from langchain.tools import tool

@tool
def fill_company_profile() -> str:
    """Start onboarding by collecting company details."""
    return "Please share your company name, size, and industry."

def get_company_agent():
    llm = ChatOpenAI(
        openai_api_key=settings.OPENAI_API_KEY,
        model="gpt-4",
        temperature=0
    )
    return initialize_agent(
        tools=[fill_company_profile],
        llm=llm,
        agent=AgentType.OPENAI_FUNCTIONS,
        verbose=True,
    )
