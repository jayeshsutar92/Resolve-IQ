from langchain_core.prompts import PromptTemplate
from pydantic import BaseModel, Field as LCField
from ai.llm import llm
from ai.langgraph.state import WorkflowState
from utils.logger import get_logger

logger = get_logger(__name__)

class IntentDetection(BaseModel):
    intent: str = LCField(description="Must be 'log', 'edit', or 'upload'")

async def detect_intent_node(state: WorkflowState) -> WorkflowState:
    logger.info("Running detect_intent_node")
    
    if state.get("document_text"):
        state["intent"] = "upload"
        return state
        
    user_input = state.get("user_input", "")
    complaint_id = state.get("complaint_id")

    if not user_input:
        state["error"] = "No input provided."
        return state

    if complaint_id:
        state["intent"] = "edit"
        return state

    prompt = PromptTemplate.from_template(
        "You are an intent classifier for a complaint management system.\n"
        "User message: {message}\n\n"
        "If the user is trying to log a new complaint, output 'log'.\n"
        "If the user is trying to edit a complaint, output 'edit'.\n"
        "Otherwise output 'log'. Only output the word."
    )
    
    structured_llm = llm.with_structured_output(IntentDetection)
    try:
        result = await structured_llm.ainvoke(prompt.format(message=user_input))
        state["intent"] = result.intent
    except Exception as e:
        logger.error(f"Intent detection failed: {e}")
        state["intent"] = "log"

    return state
