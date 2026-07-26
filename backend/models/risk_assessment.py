"""
risk_assessment.py
SQLAlchemy model for representing AI-generated risk assessments for complaints.
"""

import uuid
from typing import Optional
from sqlalchemy import String, Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID
from models.base import BaseModel

class RiskAssessment(BaseModel):
    """
    Stores the LLM-generated risk assessment for a specific complaint.
    """
    __tablename__ = "risk_assessments"

    complaint_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("complaints.id", ondelete="CASCADE"), nullable=False, unique=True
    )
    
    severity: Mapped[str] = mapped_column(String(50), nullable=False)
    priority: Mapped[str] = mapped_column(String(50), nullable=False)
    risk_level: Mapped[str] = mapped_column(String(50), nullable=False)
    reasoning: Mapped[str] = mapped_column(Text, nullable=False)
    recommended_action: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    # Relationship back to Complaint
    complaint: Mapped["Complaint"] = relationship("Complaint", back_populates="risk_assessment")
