from pydantic import BaseModel
from typing import Optional, List, Dict

class HealthResponse(BaseModel):
    status: str = "ok"

class UploadResponse(BaseModel):
    resume_id: str
    preview: str

class ResumeParseResult(BaseModel):
    name: Optional[str]
    email: Optional[str]
    phone: Optional[str]
    skills: List[str] = []
    experience: Optional[str] = None
    raw_text: Optional[str] = None

class QARequest(BaseModel):
    resume_id: str
    query: str

class QAResponse(BaseModel):
    answer: str
    sources: List[str] = []

# why? Standardized request/response models for API validation.