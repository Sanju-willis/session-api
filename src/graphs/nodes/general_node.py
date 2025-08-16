# src\graphs\nodes\general_node.py
from typing import Dict, Any
from langchain_core.messages import AIMessage
from ..agents import get_general_agent
from ..state import CustomState

async def general_node(state: CustomState) -> Dict[str, Any]:
    
    agent = get_general_agent()
    
    # Handle both dict and object (defensive coding)
    if isinstance(state, dict):
        messages = state.get("messages", [])
    else:
        messages = state.messages or []
    
    try:
        # Call agent with messages directly
        response = await agent.ainvoke({"messages": messages})
        
        # AgentExecutor returns dict with 'output' key
        agent_response = response["output"]
        
    except Exception as e:
        print(f"General agent error: {e}")
        agent_response = "Hello! I'm here to help you with any questions about your business or the Kordor platform. What can I assist you with today?"
    
    # Add AI response to existing messages
    messages.append(AIMessage(
        content=agent_response,
        name="general_agent"
    ))
    
    result = {
        "messages": messages,
        "stage": "setup_complete"
    }
    
    return result