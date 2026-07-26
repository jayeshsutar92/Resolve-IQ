"""
health.py
Health check API endpoint.
"""

from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()

class HealthResponse(BaseModel):
    status: str
    message: str

@router.get("/", response_model=HealthResponse)
async def health_check():
    """
    Basic health check endpoint to verify the API is running.
    """
    return HealthResponse(status="success", message="API is healthy.")
