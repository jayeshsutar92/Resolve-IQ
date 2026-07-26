"""
chat.py
API endpoints for natural language complaint processing (log and edit).
"""

from fastapi import APIRouter, Depends
from schemas.chat import ChatRequest, ChatResponse
from services.workflow_service import WorkflowService
from api.dependencies import get_workflow_service

router = APIRouter()

@router.post("/", response_model=ChatResponse)
async def process_chat(
    request: ChatRequest,
    workflow_service: WorkflowService = Depends(get_workflow_service)
):
    """
    Processes a natural language message from the user.
    If complaint_id is provided, updates the existing complaint.
    Otherwise, logs a new complaint.
    """
    return await workflow_service.process_chat_message(
        message=request.message,
        complaint_id=request.complaint_id
    )
