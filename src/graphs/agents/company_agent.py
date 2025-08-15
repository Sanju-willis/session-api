# src/graphs/agents/company_agent.py - REMOVE system prompt from here
from langgraph.prebuilt import create_react_agent
from langchain_openai import ChatOpenAI
from src.config import settings
from .tools.company_tools import (
    save_company_basic_info,
    save_company_contact_info,
    save_company_branding,
    save_social_links,
    get_company_progress,
    fill_company_profile,
    collect_company_info,
)

def get_company_agent():
    llm = ChatOpenAI(
        openai_api_key=settings.OPENAI_API_KEY,
        model="gpt-4",
        temperature=0,
    )

    tools = [
        fill_company_profile,
        collect_company_info,
        save_company_basic_info,
        save_company_contact_info,
        save_company_branding,
        save_social_links,
        get_company_progress,
    ]

    return create_react_agent(llm, tools)