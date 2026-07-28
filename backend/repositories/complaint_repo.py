import uuid
from typing import Optional, Sequence
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from models.complaint import Complaint
from models.risk_assessment import RiskAssessment
from schemas.complaint import ComplaintBase, RiskAssessmentBase

class ComplaintRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_id(self, complaint_id: uuid.UUID) -> Optional[Complaint]:
        stmt = select(Complaint).options(selectinload(Complaint.risk_assessment)).where(Complaint.id == complaint_id)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_all(self) -> Sequence[Complaint]:
        stmt = select(Complaint).options(selectinload(Complaint.risk_assessment)).order_by(Complaint.created_at.desc())
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def create(self, data: ComplaintBase, original_text: Optional[str] = None) -> Complaint:
        complaint = Complaint(
            original_text=original_text,
            **data.model_dump(exclude_unset=True)
        )
        self.session.add(complaint)
        await self.session.flush()
        return complaint

    async def update(self, complaint: Complaint, data: ComplaintBase, original_text: Optional[str] = None) -> Complaint:
        update_data = data.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(complaint, key, value)
            
        if original_text:
            if complaint.original_text:
                complaint.original_text += f"\n[Update]: {original_text}"
            else:
                complaint.original_text = original_text
                
        await self.session.flush()
        return complaint

    async def set_risk_assessment(self, complaint_id: uuid.UUID, data: RiskAssessmentBase) -> RiskAssessment:
        stmt = select(RiskAssessment).where(RiskAssessment.complaint_id == complaint_id)
        result = await self.session.execute(stmt)
        assessment = result.scalar_one_or_none()
        
        if assessment:
            update_data = data.model_dump()
            for key, value in update_data.items():
                setattr(assessment, key, value)
        else:
            assessment = RiskAssessment(complaint_id=complaint_id, **data.model_dump())
            self.session.add(assessment)
            
        await self.session.flush()
        return assessment
