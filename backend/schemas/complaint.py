from pydantic import BaseModel, ConfigDict, Field
from typing import Optional, Dict, Any
from uuid import UUID
from datetime import datetime

class RiskAssessmentBase(BaseModel):
    severity: str = Field(description="Severity of the complaint (e.g., Low, Medium, High, Critical)")
    priority: str = Field(description="Priority for handling (e.g., P1, P2, P3)")
    risk_level: str = Field(description="Calculated overall risk level (e.g., Low, Medium, High)")
    reasoning: str = Field(description="Proportional quality control explanation for the risk assessment")
    recommended_action: Optional[str] = Field(default=None, description="Pragmatic, realistic quality assurance recommended steps")

    model_config = ConfigDict(extra="ignore")

class RiskAssessmentResponse(RiskAssessmentBase):
    id: UUID
    complaint_id: UUID
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True, extra="ignore")

class ComplaintBase(BaseModel):
    customer_name: Optional[str] = Field(default=None, description="Name of the customer or healthcare reporter")
    issue_description: Optional[str] = Field(default=None, description="Detailed description of the defect, issue, or adverse effect")
    product_or_service: Optional[str] = Field(default=None, description="Name of the product or service involved")
    date_of_incident: Optional[str] = Field(default=None, description="Date when the incident occurred")
    
    product_strength: Optional[str] = Field(default=None, description="Strength or dosage of the product (e.g., 500mg, 10mg/ml)")
    batch_number: Optional[str] = Field(default=None, description="Lot or Batch number of the manufactured product")
    manufacturing_date: Optional[str] = Field(default=None, description="Date when the batch was manufactured")
    expiry_date: Optional[str] = Field(default=None, description="Expiration date of the product batch")
    quantity_affected: Optional[str] = Field(default=None, description="Number of units, packs, or bottles affected")
    complaint_date: Optional[str] = Field(default=None, description="Date the complaint was reported")
    complaint_type: Optional[str] = Field(default=None, description="Category of complaint (e.g., Packaging Defect, Quality, Adverse Event)")
    complaint_source: Optional[str] = Field(default=None, description="Origin of complaint (e.g., Hospital, Pharmacy, Direct Customer)")
    
    additional_details: Optional[Dict[str, Any]] = Field(default=None, description="Any extra metadata")

    model_config = ConfigDict(extra="ignore")

class ComplaintResponse(ComplaintBase):
    id: UUID
    original_text: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    risk_assessment: Optional[RiskAssessmentResponse] = None

    model_config = ConfigDict(from_attributes=True, extra="ignore")

class ComplaintExtractionSchema(ComplaintBase):
    model_config = ConfigDict(extra="ignore")
