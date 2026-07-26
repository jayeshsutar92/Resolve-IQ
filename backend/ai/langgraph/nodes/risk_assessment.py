"""
risk_assessment.py
Analyzes the extracted complaint data and generates a risk assessment.
"""

import json
from langchain_core.prompts import PromptTemplate
from schemas.complaint import RiskAssessmentBase
from ai.llm import llm
from ai.langgraph.state import WorkflowState
from utils.logger import get_logger

logger = get_logger(__name__)

async def risk_assessment_node(state: WorkflowState) -> WorkflowState:
    """
    Evaluates the risk of the complaint based on extracted data.
    """
    logger.info("Running risk_assessment_node")
    
    extracted_data = state.get("extracted_complaint_data")
    if not extracted_data:
        return state
        
    prompt = PromptTemplate.from_template(
        "You are a risk assessment expert for customer complaints.\n"
        "Analyze the following complaint data and provide a structured risk assessment.\n"
        "You must determine the severity, priority, risk_level, reasoning, and a recommended_action.\n\n"
        "COMPLAINT DATA:\n{data}"
    )
    
    try:
        structured_llm = llm.with_structured_output(RiskAssessmentBase)
        # Using ainvoke for async execution
        assessment = await structured_llm.ainvoke(prompt.format(data=json.dumps(extracted_data)))
        state["risk_assessment_data"] = assessment.model_dump(exclude_unset=True)
    except Exception as e:
        logger.error(f"Risk assessment failed: {e}")
        state["error"] = f"Risk assessment error: {str(e)}"
        
    return state
