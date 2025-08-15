# src\graphs\agents\product_agent.py
from langchain.agents import create_openai_functions_agent, AgentExecutor
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain.tools import tool
from src.config import settings

@tool
async def collect_product_info() -> str:
    """Prompt user to describe their product/service for targeting."""
    return "Tell me about your product or service so we can create effective personas."

@tool
async def save_product_details(name: str, description: str, category: str) -> str:
    """Save product information to database."""
    # Add your save logic here
    return f"Saved product: {name} in category: {category}"

@tool
async def get_product_progress() -> str:
    """Check current product setup progress."""
    # Add your progress check logic here
    return "Checking product setup progress..."

PRODUCT_PROMPT = ChatPromptTemplate.from_messages([
    ("system", """You are a product specialist. You MUST guide users through product setup step-by-step and ALWAYS use tools.

MANDATORY PROCESS:
1. FIRST: Use get_product_progress tool to check what's already completed
2. THEN: Ask for missing information one step at a time
3. ALWAYS: Use appropriate tools to save each piece of information
4. CONFIRM: Each step before moving to the next

REQUIRED STEPS TO COLLECT:
- Product names
- Product descriptions  
- Pricing information
- Product categories
- Target audience

IMPORTANT RULES:
- You MUST use tools for every interaction
- Start by checking progress with get_product_progress
- Only ask for ONE piece of information at a time
- Use save_product_details to save data
- Be conversational but systematic

Example first response: "Let me check your current product setup progress first." Then use get_product_progress tool."""),
    ("human", "{input}"),
    ("placeholder", "{agent_scratchpad}"),
])

def get_product_agent():
    llm = ChatOpenAI(
        openai_api_key=settings.OPENAI_API_KEY,
        model="gpt-4",
        temperature=0,
    )

    tools = [
        collect_product_info,
        save_product_details,
        get_product_progress,
    ]

    agent = create_openai_functions_agent(llm, tools, PRODUCT_PROMPT)
    
    return AgentExecutor(
        agent=agent,
        tools=tools,
        verbose=True,
        return_intermediate_steps=True,
        max_iterations=5,
        handle_parsing_errors=True
    )