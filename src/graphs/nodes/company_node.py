# src/graphs/nodes/company_node.py - ADD system prompt here
from typing import Dict, Any
from ..agents import get_company_agent
from src.utils import append_message

COMPANY_SYSTEM_PROMPT = """You are a company onboarding specialist. Your job is to help collect company information.

Use your available tools (fill_company_profile, collect_company_info) to:
1. Ask for company name
2. Ask for company size  
3. Ask for industry
4. Be helpful and conversational

Always use tools when helping with company setup."""

async def company_node(state: Dict[str, Any]) -> Dict[str, Any]:
    """Handle company profile onboarding"""
    agent = get_company_agent()
    messages = state.get("messages", [])
    
    # Build conversation with system message
    conversation = [("system", COMPANY_SYSTEM_PROMPT)]
    conversation.extend([(msg["role"], msg["content"]) for msg in messages])
    
    # If no user message yet, prompt for company setup
    if not any(msg["role"] == "user" for msg in messages):
        conversation.append(("user", "Help me set up my company profile"))
    
    response = await agent.ainvoke({"messages": conversation})
    final_message = response["messages"][-1].content
    
    return append_message(state, "assistant", final_message, node="company_agent", message_type="assistant")