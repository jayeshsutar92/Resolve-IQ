"""
llm.py
Initializes the LLM client (Groq) using langchain-groq.
Provides a shared instance for all AI nodes.
"""

from langchain_groq import ChatGroq
from core.config import settings

def get_llm() -> ChatGroq:
    """
    Returns an instance of ChatGroq configured with the provided API key and model.
    """
    return ChatGroq(
        api_key=settings.groq_api_key,
        model_name=settings.groq_model_name,
        temperature=0.0  # Keep temperature low for structured extraction
    )

# Shared LLM instance
llm = get_llm()
