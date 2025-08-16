# src\graphs\nodes\onboarding_node.py
from typing import Dict, Any
from langchain_core.messages import AIMessage, HumanMessage
from ..agents import get_onboarding_agent
from ..state import CustomState

async def onboarding_node(state: CustomState) -> Dict[str, Any]:
   
   
   agent = get_onboarding_agent()
   
   # Handle both dict and object (defensive coding)
   if isinstance(state, dict):
       messages = state.get("messages", [])
       stage = state.get("stage")
   else:
       messages = state.messages or []
       stage = state.stage
   
   # If user is already onboarded, handle as continuing conversation
   if stage == "onboarded":
       # This is a continuing conversation with an onboarded user
       if messages and hasattr(messages[-1], 'content'):
           user_input = messages[-1].content
       else:
           user_input = "Continue conversation"
   else:
       # This is initial onboarding
       if messages and hasattr(messages[-1], 'type') and messages[-1].type == "human":
           user_input = messages[-1].content
       else:
           user_input = "Start onboarding"
           messages.append(HumanMessage(content=user_input))
   
   
   try:
       # Call agent with messages directly
       response = await agent.ainvoke({"messages": messages})
       agent_response = response.content
       
   except Exception as e:
       print(f"DEBUG onboarding_node: Exception: {type(e).__name__}: {str(e)}")
       if stage == "onboarded":
           agent_response = "Hi! How can I help you today?"
       else:
           agent_response = "🎉 Welcome to Kordor! What's your name?"
   
   # Add AI response to existing messages
   messages.append(AIMessage(
       content=agent_response,
       name="onboarding_agent"
   ))
   
   result = {
       "messages": messages,
       "stage": "onboarded"  # Keep as onboarded
   }
   
   return result