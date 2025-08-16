# src\core\llm_client.py
from langchain_openai import ChatOpenAI
from src.config import settings

def get_llm_client(model: str = "gpt-3.5-turbo", temperature: float = 0):
    return ChatOpenAI(
        openai_api_key=settings.OPENAI_API_KEY,
        model=model,
        temperature=temperature,
    )