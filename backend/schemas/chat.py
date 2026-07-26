"""
chat.py
Pydantic schemas for the chat API endpoint.
"""

from pydantic import BaseModel, Field
from typing import Optional
from uuid import UUID
from schemas.complaint import ComplaintResponse

class ChatRequest(BaseModel):
    """
    Request schema for the /chat endpoint.
    Expects natural language text and optionally a complaint_id for editing.
    """
    message: str = Field(..., description="The natural language message from the user.")
    complaint_id: Optional[UUID] = Field(default=None, description="Provide this if editing an existing complaint.")

class ChatResponse(BaseModel):
    """
    Response schema for the /chat endpoint.
    Returns the intent detected and the current state of the complaint.
    """
    status: str = Field(default="success")
    message: str = Field(..., description="A friendly response from the system.")
    intent: str = Field(..., description="The detected intent (e.g., log_complaint, edit_complaint, document_upload).")
    complaint: Optional[ComplaintResponse] = Field(default=None, description="The updated or created complaint data.")
