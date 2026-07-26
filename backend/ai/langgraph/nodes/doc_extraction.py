"""
doc_extraction.py
Extracts complaint data from uploaded document text.
"""

from langchain_core.prompts import PromptTemplate
from schemas.complaint import ComplaintExtractionSchema
from ai.llm import llm
from ai.langgraph.state import WorkflowState
from utils.logger import get_logger

logger = get_logger(__name__)

async def doc_extraction_node(state: WorkflowState) -> WorkflowState:
    """
    Extracts complaint fields from document text.
    """
    logger.info("Running doc_extraction_node")
    
    doc_text = state.get("document_text")
    if not doc_text:
        return state
        
    prompt = PromptTemplate.from_template(
        "You are an expert at extracting structured information from formal documents.\n"
        "Extract the following fields representing a customer complaint: customer_name, issue_description, product_or_service, date_of_incident.\n"
        "If a field is not present, leave it null.\n\n"
        "DOCUMENT TEXT:\n{text}"
    )
    
    try:
        structured_llm = llm.with_structured_output(ComplaintExtractionSchema)
        extracted_data = await structured_llm.ainvoke(prompt.format(text=doc_text))
        state["extracted_complaint_data"] = extracted_data.model_dump(exclude_unset=True)
    except Exception as e:
        logger.error(f"Document extraction failed: {e}")
        state["error"] = f"Document extraction error: {str(e)}"
        
    return state
