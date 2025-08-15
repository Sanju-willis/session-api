# src\graphs\nodes\general_node.py
from typing import Dict, Any
from ..agents import get_general_agent
from src.utils import append_message

async def general_node(state: Dict[str, Any]) -> Dict[str, Any]:
    """Handle general conversations after setup is complete"""
    agent = get_general_agent()
    messages = state.get("messages", [])
    
    # Add system context to guide the agent
    system_msg = """You are a helpful assistant for the Kordor platform. 
    
Your job is to:
1. Help users with general questions about their business
2. Provide guidance on using Kordor features
3. Answer questions about their company profile and products
4. Be conversational and helpful
5. Direct users to specific modules when needed

The user has completed their initial setup. Be friendly and assist with any questions."""
    
    conversation = [("system", system_msg)]
    conversation.extend([(msg["role"], msg["content"]) for msg in messages])
    
    # If no user message yet, provide default response
    if not any(msg["role"] == "user" for msg in messages):
        conversation.append(("user", "I need help with general questions"))
    
    response = await agent.ainvoke({"messages": conversation})
    final_message = response["messages"][-1].content

    # Update state with message and append to conversation
    return append_message(
        state, 
        "assistant", 
        final_message,
        node="general_agent",
        message_type="assistant"
    )