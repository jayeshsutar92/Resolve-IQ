"""
editing.py
Applies edits to an existing complaint based on user instructions.
"""

import json
from langchain_core.prompts import PromptTemplate
from schemas.complaint import ComplaintExtractionSchema
from ai.llm import llm
from ai.langgraph.state import WorkflowState
from utils.logger import get_logger

logger = get_logger(__name__)

async def editing_node(state: WorkflowState) -> WorkflowState:
    """
    Updates an existing complaint based on new user input.
    """
    logger.info("Running editing_node")
    
    user_input = state.get("user_input")
    current_record = state.get("current_complaint_record")
    
    if not user_input or not current_record:
        state["error"] = "Missing input or current record for editing."
        return state
        
    current_data_str = json.dumps({
        "customer_name": current_record.customer_name,
        "issue_description": current_record.issue_description,
        "product_or_service": current_record.product_or_service,
        "date_of_incident": current_record.date_of_incident
    })
        
    prompt = PromptTemplate.from_template(
        "You are an expert at updating structured customer complaints.\n"
        "Given the CURRENT DATA and the user's UPDATE INSTRUCTIONS, output the fully updated structured data.\n"
        "Preserve existing values unless the user instructions explicitly change them.\n\n"
        "CURRENT DATA:\n{current_data}\n\n"
        "UPDATE INSTRUCTIONS:\n{instructions}"
    )
    
    try:
        structured_llm = llm.with_structured_output(ComplaintExtractionSchema)
        updated_data = await structured_llm.ainvoke(
            prompt.format(current_data=current_data_str, instructions=user_input)
        )
        state["extracted_complaint_data"] = updated_data.model_dump(exclude_unset=True)
    except Exception as e:
        logger.error(f"Editing failed: {e}")
        state["error"] = f"Editing error: {str(e)}"
        
    return state
