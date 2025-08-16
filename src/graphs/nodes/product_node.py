# src\graphs\nodes\product_node.py
from typing import Dict, Any
from langchain_core.messages import AIMessage
from ..agents import get_product_agent
from ..state import CustomState

async def product_node(state: CustomState) -> Dict[str, Any]:
    
    agent = get_product_agent()
    
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
        print(f"Product agent error: {e}")
        agent_response = "Let me help you set up your products. First, let me check what information we already have."
    
    # Add AI response to existing messages
    messages.append(AIMessage(
        content=agent_response,
        name="product_agent"
    ))
    
    result = {
        "messages": messages,
        "stage": "company_completed"
    }
    
    return result