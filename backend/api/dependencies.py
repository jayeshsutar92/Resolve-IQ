from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from database.session import get_db_session
from services.workflow_service import WorkflowService
from repositories.complaint_repo import ComplaintRepository

async def get_workflow_service(session: AsyncSession = Depends(get_db_session)) -> WorkflowService:
    return WorkflowService(session)

async def get_complaint_repo(session: AsyncSession = Depends(get_db_session)) -> ComplaintRepository:
    return ComplaintRepository(session)
