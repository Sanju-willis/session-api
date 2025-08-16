# src\graphs\nodes\company_node.py
from typing import Dict, Any
from langchain_core.messages import AIMessage
from ..agents import get_company_agent
from ..state import CustomState

async def company_node(state: CustomState) -> Dict[str, Any]:
    
    agent = get_company_agent()
    
    # Handle both dict and object (defensive coding)
    if isinstance(state, dict):
        messages = state.get("messages", [])
    else:
        messages = state.messages or []
    
    try:
        # Call agent with messages directly
        response = await agent.ainvoke({"messages": messages})
        
        # AgentExecutor returns dict with 'output' key
        agent_response = response["output"]  # ← Changed from response.content
        
    except Exception as e:
        print(f"Company agent error: {e}")
        agent_response = "I'm sorry, I encountered an error. Let me help you set up your company profile. What's your company name?"
    
    # Add AI response to existing messages
    messages.append(AIMessage(
        content=agent_response,
        name="company_agent"
    ))
    
    result = {
        "messages": messages,
        "stage": "need_company"
    }
    
    return result