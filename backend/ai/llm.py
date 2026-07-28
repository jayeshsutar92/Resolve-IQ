from langchain_groq import ChatGroq
from core.config import settings

def get_llm() -> ChatGroq:
    return ChatGroq(
        api_key=settings.groq_api_key,
        model_name=settings.groq_model_name,
        temperature=0.0
    )

llm = get_llm()
