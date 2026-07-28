from pydantic import BaseModel, Field
from typing import Optional
from uuid import UUID
from schemas.complaint import ComplaintResponse

class ChatRequest(BaseModel):
    message: str = Field(..., description="The natural language message from the user.")
    complaint_id: Optional[UUID] = Field(default=None, description="Provide this if editing an existing complaint.")

class ChatResponse(BaseModel):
    status: str = Field(default="success")
    message: str = Field(..., description="A friendly response from the system.")
    intent: str = Field(..., description="The detected intent (e.g., log_complaint, edit_complaint, document_upload).")
    complaint: Optional[ComplaintResponse] = Field(default=None, description="The updated or created complaint data.")
