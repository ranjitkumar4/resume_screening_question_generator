# Why: FR-01 and FR-02.

from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from backend.app.schemas import UploadResponse, ResumeParseResult
from backend.app.services.resume_parser import store_resume_text, parse_resume_simple
from backend.app.utils.logger import get_logger

router = APIRouter(prefix="/resume")
logger = get_logger("resume_routes")

@router.post("/upload", response_model=UploadResponse)
async def upload_resume(file: UploadFile = File(...)):
    """
    Accept uploaded file (text or other types). For now we only accept text/plain.
    Return a resume_id and preview.
    """
    contents = await file.read()
    try:
        text = contents.decode("utf-8", errors="ignore")
    except Exception:
        raise HTTPException(status_code=400, detail="Could not decode file.")
    resume_id = store_resume_text(text)
    preview = text[:500]
    return UploadResponse(resume_id=resume_id, preview=preview)

@router.get("/parse/{resume_id}", response_model=ResumeParseResult)
def parse_resume(resume_id: str):
    parsed = parse_resume_simple(resume_id)
    return parsed