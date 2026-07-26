"""
complaint_repo.py
Repository pattern for handling database operations for Complaints and Risk Assessments.
"""

import uuid
from typing import Optional, Sequence
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from models.complaint import Complaint
from models.risk_assessment import RiskAssessment
from schemas.complaint import ComplaintBase, RiskAssessmentBase

class ComplaintRepository:
    """
    Handles all DB interactions for Complaints.
    """
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_id(self, complaint_id: uuid.UUID) -> Optional[Complaint]:
        """
        Retrieves a complaint by its ID, including its risk assessment.
        """
        stmt = select(Complaint).options(selectinload(Complaint.risk_assessment)).where(Complaint.id == complaint_id)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_all(self) -> Sequence[Complaint]:
        """
        Retrieves all complaints.
        """
        stmt = select(Complaint).options(selectinload(Complaint.risk_assessment)).order_by(Complaint.created_at.desc())
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def create(self, data: ComplaintBase, original_text: Optional[str] = None) -> Complaint:
        """
        Creates a new complaint.
        """
        complaint = Complaint(
            original_text=original_text,
            **data.model_dump(exclude_unset=True)
        )
        self.session.add(complaint)
        await self.session.flush()
        return complaint

    async def update(self, complaint: Complaint, data: ComplaintBase, original_text: Optional[str] = None) -> Complaint:
        """
        Updates an existing complaint with new data.
        """
        update_data = data.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(complaint, key, value)
            
        if original_text:
            # Append new text to original text or replace? We can just append for history.
            if complaint.original_text:
                complaint.original_text += f"\n[Update]: {original_text}"
            else:
                complaint.original_text = original_text
                
        await self.session.flush()
        return complaint

    async def set_risk_assessment(self, complaint_id: uuid.UUID, data: RiskAssessmentBase) -> RiskAssessment:
        """
        Creates or updates the risk assessment for a complaint.
        """
        stmt = select(RiskAssessment).where(RiskAssessment.complaint_id == complaint_id)
        result = await self.session.execute(stmt)
        assessment = result.scalar_one_or_none()
        
        if assessment:
            # Update
            update_data = data.model_dump()
            for key, value in update_data.items():
                setattr(assessment, key, value)
        else:
            # Create
            assessment = RiskAssessment(complaint_id=complaint_id, **data.model_dump())
            self.session.add(assessment)
            
        await self.session.flush()
        return assessment
