"""
complaint.py
Pydantic schemas for Complaint and Risk Assessment for validation and serialization.
"""

from pydantic import BaseModel, ConfigDict, Field
from typing import Optional, Dict, Any
from uuid import UUID
from datetime import datetime

class RiskAssessmentBase(BaseModel):
    """Base schema for Risk Assessment"""
    severity: str = Field(description="Severity of the complaint (e.g., Low, Medium, High)")
    priority: str = Field(description="Priority for handling (e.g., P1, P2, P3)")
    risk_level: str = Field(description="Calculated overall risk level")
    reasoning: str = Field(description="Explanation for the risk assessment")
    recommended_action: Optional[str] = Field(default=None, description="Suggested next steps")

class RiskAssessmentResponse(RiskAssessmentBase):
    """Schema for Risk Assessment returned to the client"""
    id: UUID
    complaint_id: UUID
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)

class ComplaintBase(BaseModel):
    """Base schema for Complaint"""
    customer_name: Optional[str] = Field(default=None, description="Name of the customer")
    issue_description: Optional[str] = Field(default=None, description="Detailed description of the issue")
    product_or_service: Optional[str] = Field(default=None, description="Product or service involved")
    date_of_incident: Optional[str] = Field(default=None, description="Date when the incident occurred")
    additional_details: Optional[Dict[str, Any]] = Field(default=None, description="Any other extracted info")

class ComplaintResponse(ComplaintBase):
    """Schema for Complaint returned to the client"""
    id: UUID
    original_text: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    risk_assessment: Optional[RiskAssessmentResponse] = None

    model_config = ConfigDict(from_attributes=True)

class ComplaintExtractionSchema(ComplaintBase):
    """Schema used by LLM to output structured complaint data"""
    # Inherits fields from ComplaintBase. LLM will use this as a target schema.
    pass
