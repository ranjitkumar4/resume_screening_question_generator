# Why: FR-05 & FR-06 initial implementation.

from typing import List
from backend.app.utils.logger import get_logger
from backend.app.services.resume_parser import parse_resume_simple, get_raw_resume

logger = get_logger("qgen")

def generate_questions_from_resume(resume_id: str, jd_text: str) -> List[str]:
    """
    Generate a small set of questions using resume skills & JD keywords.
    Replace with LLM-driven generation later.
    """
    parsed = parse_resume_simple(resume_id)
    skills = parsed.skills or []
    questions = []
    # Technical
    for s in skills[:4]:
        questions.append(f"Technical: Describe a project where you used {s}. What challenges did you face and how did you solve them?")
    # Behavioral: from JD keywords
    if "team" in (jd_text or "").lower():
        questions.append("Behavioral: Tell me about a time you collaborated with a team to overcome a difficult problem.")
    else:
        questions.append("Behavioral: Describe a difficult decision you took in a previous role and why.")
    return questions