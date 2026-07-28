from typing import List
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from schemas.complaint import ComplaintResponse
from repositories.complaint_repo import ComplaintRepository
from api.dependencies import get_complaint_repo

router = APIRouter()

@router.get("/", response_model=List[ComplaintResponse])
async def list_complaints(repo: ComplaintRepository = Depends(get_complaint_repo)):
    return await repo.get_all()

@router.get("/{complaint_id}", response_model=ComplaintResponse)
async def get_complaint(
    complaint_id: UUID,
    repo: ComplaintRepository = Depends(get_complaint_repo)
):
    complaint = await repo.get_by_id(complaint_id)
    if not complaint:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Complaint not found")
    return complaint
