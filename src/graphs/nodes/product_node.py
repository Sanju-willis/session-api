# src\graphs\nodes\product_node.py
from typing import Dict, Any
from ..agents import get_product_agent
from src.utils import append_message


async def product_node(state: Dict[str, Any]) -> Dict[str, Any]:
    """Handle product information collection with multi-step guidance"""
    agent = get_product_agent()
    messages = state.get("messages", [])

    # Get the latest user message or provide default
    if messages:
        user_input = messages[-1]["content"] if messages[-1]["role"] == "user" else "Start my product setup"
    else:
        user_input = "Start my product setup"

    try:
        response = await agent.ainvoke(
            {"input": user_input, "chat_history": [(msg["role"], msg["content"]) for msg in messages[:-1] if messages]}
        )

        final_message = response["output"]

        # Check if agent used tools
        steps_used = len(response.get("intermediate_steps", []))
        print(f"Product agent used {steps_used} steps")

        # If no tools used, prompt more specifically
        if steps_used == 0 and not messages:
            final_message = (
                "Let me check your current product setup progress first, then guide you through adding your products."
            )

    except Exception as e:
        print(f"Error in product agent: {e}")
        final_message = "Let me help you set up your products. First, let me check what information we already have."

    return append_message(state, "assistant", final_message, node="product_agent", message_type="assistant")
