# src\graphs\nodes\company_node.py
from typing import Dict, Any
from ..agents import get_company_agent
from src.utils import append_message

async def company_node(state: Dict[str, Any]) -> Dict[str, Any]:
   agent = get_company_agent()
   messages = state.get("messages", [])
   
   # Get the latest user message or provide default
   if messages:
       # Use existing conversation
       user_input = messages[-1]["content"] if messages[-1]["role"] == "user" else "Help me set up my company profile"
   else:
       # First interaction
       user_input = "Help me set up my company profile"
   
   try:
       # Invoke the agent with proper input format
       response = await agent.ainvoke({
           "input": user_input,
           "chat_history": [
               (msg["role"], msg["content"]) 
               for msg in messages[:-1] if messages  # Exclude the current message
           ]
       })
       
       # Extract the final response
       final_message = response["output"]
       
       # Log intermediate steps if available (for debugging)
       if "intermediate_steps" in response:
           print(f"Agent used {len(response['intermediate_steps'])} steps")
       
   except Exception as e:
       print(f"Error in company agent: {e}")
       final_message = "I'm sorry, I encountered an error. Let me help you set up your company profile. What's your company name?"
   
   # Update state with assistant response
   return append_message(
       state, 
       "assistant", 
       final_message, 
       node="company_agent", 
       message_type="assistant"
   )