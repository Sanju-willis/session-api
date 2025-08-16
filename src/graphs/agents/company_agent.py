# src\graphs\agents\company_agent.py
from langchain.agents import create_openai_functions_agent, AgentExecutor
from langchain_core.prompts import ChatPromptTemplate
from src.core.llm_client import get_llm_client

from .tools.company_tools import (
    save_company_basic_info,
    save_company_contact_info,
    save_company_branding,
    save_social_links,
    get_company_progress,
    fill_company_profile,
    collect_company_info,
)

COMPANY_PROMPT = ChatPromptTemplate.from_messages([
    ("system", """You are a company onboarding specialist. Your job is to guide users through company setup step-by-step.

CAPABILITIES:
- Use tools to save/retrieve company information
- Check user progress and memory using existing tools
- Guide users through multi-step processes
- Be conversational and helpful

PROCESS:
1. Check existing progress first
2. Ask for missing information step by step
3. Use tools to save data
4. Confirm each step before moving on

TOOLS AVAILABLE:
- fill_company_profile: Save company data
- collect_company_info: Get company details
- get_company_progress: Check what's completed

Always check progress first, then guide step by step."""),
    ("human", "{input}"),
    ("placeholder", "{agent_scratchpad}"),
])

def get_company_agent():
    llm = get_llm_client()

    tools = [
        fill_company_profile,
        collect_company_info,
        get_company_progress,
        save_company_basic_info,
        save_company_contact_info,
        save_company_branding,
        save_social_links,
    ]

    agent = create_openai_functions_agent(llm, tools, COMPANY_PROMPT)
    
    return AgentExecutor(
        agent=agent,
        tools=tools,
        verbose=True,
        return_intermediate_steps=True,
        max_iterations=5,
        handle_parsing_errors=True
    )