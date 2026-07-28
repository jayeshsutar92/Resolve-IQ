from typing import TypedDict, Optional, Any, Dict
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession

class WorkflowState(TypedDict, total=False):
    user_input: Optional[str]
    document_text: Optional[str]
    complaint_id: Optional[UUID]
    db_session: Optional[AsyncSession]
    
    intent: Optional[str]
    extracted_complaint_data: Optional[Dict[str, Any]]
    risk_assessment_data: Optional[Dict[str, Any]]
    saved_complaint: Optional[Any]
    
    error: Optional[str]
    current_complaint_record: Optional[Any]
