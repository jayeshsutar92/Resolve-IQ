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
    return await workflow_service.process_chat_message(
        message=request.message,
        complaint_id=request.complaint_id
    )
