# src\graphs\nodes\product_node.py
from typing import Dict, Any
from ..agents import get_product_agent
from src.utils import append_message


async def product_node(state: Dict[str, Any]) -> Dict[str, Any]:
    """Handle product information collection"""
    agent = get_product_agent()
    messages = state.get("messages", [])

    # Add system context for product collection
    system_msg = """You are a product specialist. Help collect product information including:
1. Product names
2. Product descriptions
3. Pricing
4. Categories

Be helpful and use your tools appropriately."""

    conversation = [("system", system_msg)]
    conversation.extend([(msg["role"], msg["content"]) for msg in messages])

    response = await agent.ainvoke({"messages": conversation})
    final_message = response["messages"][-1].content

    # Update state with message and append to conversation
    return append_message(state, "assistant", final_message, node="product_agent", message_type="assistant")
