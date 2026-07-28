from ai.langgraph.state import WorkflowState
from repositories.complaint_repo import ComplaintRepository
from schemas.complaint import ComplaintBase, RiskAssessmentBase
from utils.logger import get_logger

logger = get_logger(__name__)

async def db_save_node(state: WorkflowState) -> WorkflowState:
    logger.info("Running db_save_node")
    
    session = state.get("db_session")
    extracted_data = state.get("extracted_complaint_data")
    risk_data = state.get("risk_assessment_data")
    intent = state.get("intent")
    user_input = state.get("user_input") or state.get("document_text", "")
    current_record = state.get("current_complaint_record")

    if not session:
        logger.warning("No db_session provided in state; skipping db_save_node execution.")
        return state

    if not extracted_data:
        state["error"] = "No extracted complaint data available to save."
        return state

    try:
        repo = ComplaintRepository(session)
        complaint_schema = ComplaintBase(**extracted_data)
        
        if intent == "edit" and current_record:
            complaint = await repo.update(current_record, complaint_schema, original_text=user_input)
        else:
            complaint = await repo.create(complaint_schema, original_text=user_input)

        if risk_data:
            risk_schema = RiskAssessmentBase(**risk_data)
            await repo.set_risk_assessment(complaint.id, risk_schema)

        await session.commit()

        updated_record = await repo.get_by_id(complaint.id)
        state["saved_complaint"] = updated_record
        logger.info(f"Successfully saved and committed complaint {complaint.id} to database.")
    except Exception as e:
        await session.rollback()
        logger.error(f"Database save failed: {e}", exc_info=True)
        state["error"] = f"Database save error: {str(e)}"

    return state
