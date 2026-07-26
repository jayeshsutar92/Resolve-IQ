"""
complaint.py
SQLAlchemy model for representing user complaints in the database.
"""

from typing import Optional, List
from sqlalchemy import String, Text, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship
from models.base import BaseModel

class Complaint(BaseModel):
    """
    Represents a complaint logged by a user or extracted from a document.
    """
    __tablename__ = "complaints"

    # We store the raw natural language input or document text for context
    original_text: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    
    # Extracted fields
    customer_name: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    issue_description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    product_or_service: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    date_of_incident: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    
    # We can store any additional extracted properties in a flexible JSON column
    additional_details: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)

    # Relationship to Risk Assessment
    risk_assessment: Mapped[Optional["RiskAssessment"]] = relationship(
        "RiskAssessment", back_populates="complaint", cascade="all, delete-orphan", uselist=False
    )
