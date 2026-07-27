"""
editing.py
Applies edits to an existing complaint based on user instructions while preserving untouched fields.
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
    Updates an existing complaint based on new user input while preserving existing fields.
    """
    logger.info("Running editing_node")
    
    user_input = state.get("user_input")
    current_record = state.get("current_complaint_record")
    
    if not user_input or not current_record:
        state["error"] = "Missing input or current record for editing."
        return state
        
    current_dict = {
        "customer_name": current_record.customer_name,
        "issue_description": current_record.issue_description,
        "product_or_service": current_record.product_or_service,
        "date_of_incident": current_record.date_of_incident,
        "product_strength": current_record.product_strength,
        "batch_number": current_record.batch_number,
        "manufacturing_date": current_record.manufacturing_date,
        "expiry_date": current_record.expiry_date,
        "quantity_affected": current_record.quantity_affected,
        "complaint_date": current_record.complaint_date,
        "complaint_type": current_record.complaint_type,
        "complaint_source": current_record.complaint_source,
    }
        
    prompt = PromptTemplate.from_template(
        "You are an expert at updating structured customer complaint records.\n"
        "Given the CURRENT RECORD and the UPDATE INSTRUCTIONS, output the updated complaint schema.\n\n"
        "RULES:\n"
        "1. Update ONLY the fields mentioned in the update instructions.\n"
        "2. PRESERVE all other existing values exactly as they are in the CURRENT RECORD.\n"
        "3. Do NOT set any field to null unless the user explicitly requests deleting or clearing it.\n\n"
        "CURRENT RECORD:\n{current_data}\n\n"
        "UPDATE INSTRUCTIONS:\n{instructions}"
    )
    
    try:
        structured_llm = llm.with_structured_output(ComplaintExtractionSchema)
        updated_model = await structured_llm.ainvoke(
            prompt.format(current_data=json.dumps(current_dict, indent=2), instructions=user_input)
        )
        updated_dict = updated_model.model_dump(exclude_unset=True)
        
        # Merge updated fields over current dictionary to strictly guarantee non-mentioned fields are preserved
        merged_data = {**current_dict}
        for k, v in updated_dict.items():
            if v is not None or (k in user_input.lower() and ("remove" in user_input.lower() or "clear" in user_input.lower())):
                merged_data[k] = v
                
        state["extracted_complaint_data"] = merged_data
    except Exception as e:
        logger.error(f"Editing failed: {e}")
        state["error"] = f"Editing error: {str(e)}"
        
    return state
