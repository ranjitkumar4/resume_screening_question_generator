from fastapi import APIRouter
from backend.app.schemas import HealthResponse

router = APIRouter()

@router.get("/health", response_model=HealthResponse)
def health():
    """Simple health check endpoint."""
    return HealthResponse(status="ok")