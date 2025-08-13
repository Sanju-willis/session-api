# src\graphs\agents\product_agent.py
from src.config.settings import settings
from langchain.agents import initialize_agent, AgentType
from langchain_openai import ChatOpenAI
from langchain.tools import tool

@tool
def collect_product_info() -> str:
    """Prompt user to describe their product/service for targeting."""
    return "Tell me about your product or service so we can create effective personas."

def get_product_agent():
    llm = ChatOpenAI(
        openai_api_key=settings.OPENAI_API_KEY,
        model="gpt-4",
        temperature=0
    )
    return initialize_agent(
        tools=[collect_product_info],
        llm=llm,
        agent=AgentType.OPENAI_FUNCTIONS,
        verbose=True,
    )
