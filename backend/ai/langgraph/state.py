"""
state.py
Defines the State TypedDict for the LangGraph workflow.
"""

from typing import TypedDict, Optional, Any, Dict
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession

class WorkflowState(TypedDict, total=False):
    """
    The state structure passed around between LangGraph nodes.
    """
    # Inputs
    user_input: Optional[str]
    document_text: Optional[str]
    complaint_id: Optional[UUID]
    db_session: Optional[AsyncSession]
    
    # Processed Data
    intent: Optional[str]  # e.g., 'log', 'edit', 'upload'
    extracted_complaint_data: Optional[Dict[str, Any]]
    risk_assessment_data: Optional[Dict[str, Any]]
    saved_complaint: Optional[Any]
    
    # Execution Flags/Context
    error: Optional[str]
    current_complaint_record: Optional[Any]  # Used when editing
