"""
extraction.py
Extracts complaint data from natural language into structured JSON.
"""

from langchain_core.prompts import PromptTemplate
from schemas.complaint import ComplaintExtractionSchema
from ai.llm import llm
from ai.langgraph.state import WorkflowState
from utils.logger import get_logger

logger = get_logger(__name__)

async def extraction_node(state: WorkflowState) -> WorkflowState:
    """
    Extracts complaint fields from user input.
    """
    logger.info("Running extraction_node")
    user_input = state.get("user_input")
    
    if not user_input:
        return state
        
    prompt = PromptTemplate.from_template(
        "You are an expert at extracting structured information from customer complaints.\n"
        "Extract the following fields if present: customer_name, issue_description, product_or_service, date_of_incident.\n"
        "If a field is not mentioned, leave it null.\n\n"
        "Complaint text:\n{message}"
    )
    
    try:
        structured_llm = llm.with_structured_output(ComplaintExtractionSchema)
        extracted_data = await structured_llm.ainvoke(prompt.format(message=user_input))
        state["extracted_complaint_data"] = extracted_data.model_dump(exclude_unset=True)
    except Exception as e:
        logger.error(f"Extraction failed: {e}")
        state["error"] = f"Extraction error: {str(e)}"
        
    return state
