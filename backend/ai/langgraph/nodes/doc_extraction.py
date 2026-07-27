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
        "You are an expert pharmaceutical compliance officer.\n"
        "Extract structured complaint fields from the following formal document:\n"
        "- customer_name (reporter or patient name)\n"
        "- issue_description (detailed issue description)\n"
        "- product_or_service (drug/product name)\n"
        "- date_of_incident (incident date)\n"
        "- product_strength (e.g., 500mg, 10mg/ml)\n"
        "- batch_number (lot or batch ID)\n"
        "- manufacturing_date\n"
        "- expiry_date\n"
        "- quantity_affected\n"
        "- complaint_date\n"
        "- complaint_type (e.g., Packaging Defect, Adverse Event, Product Quality)\n"
        "- complaint_source (e.g., Hospital, Retail Pharmacy, Consumer)\n"
        "Leave fields as null if not found in the document.\n\n"
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
