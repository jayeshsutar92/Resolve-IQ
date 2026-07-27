"""
complaint.py
SQLAlchemy model for representing user complaints in the database.
"""

from typing import Optional
from sqlalchemy import String, Text, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship
from models.base import BaseModel

class Complaint(BaseModel):
    """
    Represents a complaint logged by a user or extracted from a document.
    """
    __tablename__ = "complaints"

    # Raw input text or document content
    original_text: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    
    # Standard complaint fields
    customer_name: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    issue_description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    product_or_service: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    date_of_incident: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    
    # Extended product & complaint fields
    product_strength: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    batch_number: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    manufacturing_date: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    expiry_date: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    quantity_affected: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    complaint_date: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    complaint_type: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    complaint_source: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)

    # Additional metadata
    additional_details: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)

    # Relationship to Risk Assessment
    risk_assessment: Mapped[Optional["RiskAssessment"]] = relationship(
        "RiskAssessment", back_populates="complaint", cascade="all, delete-orphan", uselist=False
    )
