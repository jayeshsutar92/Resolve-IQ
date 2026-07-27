"""
risk_assessment.py
Analyzes the extracted complaint data and generates a proportional, realistic risk assessment.
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
    Evaluates the risk of the complaint based on extracted data, generating balanced and realistic recommendations.
    """
    logger.info("Running risk_assessment_node")
    
    extracted_data = state.get("extracted_complaint_data")
    if not extracted_data:
        return state
        
    prompt = PromptTemplate.from_template(
        "You are a Quality Assurance and Risk Assessment Specialist in pharmaceuticals & healthcare.\n"
        "Analyze the complaint issue details below and generate a realistic, proportional, and actionable risk assessment.\n\n"
        "GUIDELINES:\n"
        "- severity: Assign Low, Medium, High, or Critical based on patient/user safety risk.\n"
        "- priority: Assign P1 (Urgent/Critical), P2 (Major issue needing rapid review), or P3 (Minor issue/inquiry).\n"
        "- risk_level: Low, Medium, or High.\n"
        "- reasoning: Provide a clear, objective Quality Control explanation based strictly on the facts.\n"
        "- recommended_action: Provide pragmatic, realistic recommended Quality Control or CAPA steps.\n"
        "  IMPORTANT: Avoid overly aggressive measures (such as immediate global product recalls or plant shutdowns)\n"
        "  unless there is explicit evidence of life-threatening harm, critical contamination, or systemic hazard.\n"
        "  For minor issues (e.g. damaged outer box, minor delay), recommend standard investigation, retain sample testing, or customer replacement.\n\n"
        "CRITICAL INSTRUCTION: Output ONLY the 5 required fields: severity, priority, risk_level, reasoning, recommended_action.\n"
        "Do NOT include any extra keys such as product_or_service, customer_name, or batch_number.\n\n"
        "COMPLAINT DETAILS:\n{data}"
    )
    
    # Filter data for prompt to prevent LLM from echoing non-risk fields into tool parameters
    risk_input_data = {
        "issue_description": extracted_data.get("issue_description"),
        "complaint_type": extracted_data.get("complaint_type"),
        "quantity_affected": extracted_data.get("quantity_affected"),
        "date_of_incident": extracted_data.get("date_of_incident")
    }
    
    try:
        structured_llm = llm.with_structured_output(RiskAssessmentBase)
        assessment = await structured_llm.ainvoke(prompt.format(data=json.dumps(risk_input_data, indent=2)))
        state["risk_assessment_data"] = assessment.model_dump(exclude_unset=True)
    except Exception as e:
        logger.error(f"Risk assessment failed: {e}")
        state["error"] = f"Risk assessment error: {str(e)}"
        
    return state
