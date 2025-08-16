# src\graphs\nodes\general_node.py
from typing import Dict, Any
from ..agents import get_general_agent
from src.utils import append_message

async def general_node(state: Dict[str, Any]) -> Dict[str, Any]:

    agent = get_general_agent()
    messages = state.get("messages", [])
    
    # Get the latest user message or provide default
    if messages:
        user_input = messages[-1]["content"] if messages[-1]["role"] == "user" else "I need help with general questions"
    else:
        user_input = "How can I help you with your Kordor platform today?"
    
    try:
        response = await agent.ainvoke({
            "input": user_input,
            "chat_history": [
                (msg["role"], msg["content"]) 
                for msg in messages[:-1] if messages
            ]
        })
        
        final_message = response["output"]
        
        # Log tool usage
        steps_used = len(response.get("intermediate_steps", []))
        print(f"General agent used {steps_used} steps")
        
    except Exception as e:
        print(f"Error in general agent: {e}")
        final_message = "Hello! I'm here to help you with any questions about your business or the Kordor platform. What can I assist you with today?"
    
    return append_message(
        state, 
        "assistant", 
        final_message, 
        node="general_agent", 
        message_type="assistant"
    )