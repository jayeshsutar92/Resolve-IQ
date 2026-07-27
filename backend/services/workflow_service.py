"""
workflow_service.py
Service layer bridging API endpoints and the LangGraph AI workflow.
"""

import uuid
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status

from ai.langgraph.graph import complaint_graph
from ai.langgraph.state import WorkflowState
from repositories.complaint_repo import ComplaintRepository
from schemas.complaint import ComplaintResponse
from utils.logger import get_logger

logger = get_logger(__name__)

class WorkflowService:
    """
    Handles execution of the LangGraph workflow and coordinates with the database repository.
    """
    def __init__(self, session: AsyncSession):
        self.repo = ComplaintRepository(session)
        self.session = session

    async def process_chat_message(self, message: str, complaint_id: Optional[uuid.UUID] = None) -> dict:
        """
        Executes the main chat workflow for logging or editing complaints.
        """
        initial_state: WorkflowState = {
            "user_input": message,
            "document_text": None,
            "complaint_id": complaint_id,
            "db_session": self.session,
            "intent": None,
            "extracted_complaint_data": None,
            "risk_assessment_data": None,
            "error": None,
            "current_complaint_record": None
        }

        # If editing an existing complaint, fetch the current record first
        if complaint_id:
            record = await self.repo.get_by_id(complaint_id)
            if not record:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Complaint not found")
            initial_state["current_complaint_record"] = record

        # Run LangGraph workflow
        final_state = await complaint_graph.ainvoke(initial_state)

        if final_state.get("error"):
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=final_state["error"]
            )

        return self._format_response(final_state)

    async def process_document(self, document_text: str) -> dict:
        """
        Executes the document extraction workflow.
        """
        initial_state: WorkflowState = {
            "user_input": None,
            "document_text": document_text,
            "complaint_id": None,
            "db_session": self.session,
            "intent": None,
            "extracted_complaint_data": None,
            "risk_assessment_data": None,
            "error": None,
            "current_complaint_record": None
        }

        final_state = await complaint_graph.ainvoke(initial_state)

        if final_state.get("error"):
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=final_state["error"]
            )

        return self._format_response(final_state)

    def _format_response(self, state: WorkflowState) -> dict:
        """
        Formats the API response payload with a comprehensive summary message.
        """
        intent = state.get("intent")
        saved_record = state.get("saved_complaint")

        if not saved_record:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to retrieve saved complaint record."
            )

        # Build detailed informative AI message
        summary_lines = []
        if intent == "edit":
            summary_lines.append("I have updated the complaint with your specified changes:")
        elif intent == "upload":
            summary_lines.append("I have extracted the following complaint details from the uploaded document:")
        else:
            summary_lines.append("I have logged your complaint and extracted the following information:")

        fields_summary = []
        if saved_record.customer_name:
            fields_summary.append(f"• Customer: {saved_record.customer_name}")
        if saved_record.product_or_service:
            prod_str = saved_record.product_or_service
            if saved_record.product_strength:
                prod_str += f" ({saved_record.product_strength})"
            fields_summary.append(f"• Product: {prod_str}")
        if saved_record.batch_number:
            fields_summary.append(f"• Batch Number: {saved_record.batch_number}")
        if saved_record.date_of_incident:
            fields_summary.append(f"• Date of Incident: {saved_record.date_of_incident}")
        if saved_record.issue_description:
            desc = saved_record.issue_description
            if len(desc) > 100:
                desc = desc[:97] + "..."
            fields_summary.append(f"• Issue: {desc}")
        if saved_record.complaint_type:
            fields_summary.append(f"• Category: {saved_record.complaint_type}")

        if fields_summary:
            summary_lines.extend(fields_summary)

        if saved_record.risk_assessment:
            ra = saved_record.risk_assessment
            summary_lines.append(f"\nAI Risk Assessment: {ra.severity} Severity | Priority: {ra.priority} | Level: {ra.risk_level}")

        response_msg = "\n".join(summary_lines)

        return {
            "status": "success",
            "message": response_msg,
            "intent": intent,
            "complaint": ComplaintResponse.model_validate(saved_record)
        }
