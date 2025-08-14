# src\graphs\agents\product_agent.py
from langchain.tools import tool
from langgraph.prebuilt import create_react_agent
from langchain_openai import ChatOpenAI
from src.config.settings import settings

@tool
async def collect_product_info() -> str:
    """Prompt user to describe their product/service for targeting."""
    return "Tell me about your product or service so we can create effective personas."

def get_product_agent():
    llm = ChatOpenAI(
        openai_api_key=settings.OPENAI_API_KEY,
        model="gpt-4",
        temperature=0,
    )
    return create_react_agent(llm, [collect_product_info])

