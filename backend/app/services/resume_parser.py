## Why: We need a way to store resumes and parse them to produce structured fields per FR-02.

import uuid
from typing import Dict
from backend.app.utils.logger import get_logger
from backend.app.schemas import ResumeParseResult

logger = get_logger("resume_parser")

# Simple in-memory store for uploaded resumes (demo)
_RESUME_STORE: Dict[str, Dict] = {}

def store_resume_text(text: str) -> str:
    """
    Store raw resume text and return ID.
    """
    resume_id = str(uuid.uuid4())
    _RESUME_STORE[resume_id] = {"raw_text": text}
    logger.info("Stored resume id=%s", resume_id)
    return resume_id

def parse_resume_simple(resume_id: str) -> ResumeParseResult:
    """
    Very simple keyword-based parser that returns names, skills, etc.
    Replace with LLM-based parsing for production.
    """
    raw = _RESUME_STORE.get(resume_id, {}).get("raw_text", "")
    # naive parsing: look for emails, phones (omitted for brevity), skills lookups
    skills = []
    keywords = ["python", "sql", "docker", "aws", "spark", "pandas", "ml", "java", "business", "c", "database"]
    text_lower = raw.lower()
    for k in keywords:
        if k in text_lower:
            skills.append(k)
    result = ResumeParseResult(
        name=None,
        email=None,
        phone=None,
        skills=skills,
        experience=None,
        raw_text=raw
    )
    return result

def get_raw_resume(resume_id: str) -> str:
    return _RESUME_STORE.get(resume_id, {}).get("raw_text", "")