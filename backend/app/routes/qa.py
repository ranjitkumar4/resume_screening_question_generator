# Why: FR-05 / FR-06, shows RAG-style output (sources).

from fastapi import APIRouter, HTTPException
from backend.app.schemas import QARequest, QAResponse
from backend.app.services.qgen import generate_questions_from_resume
from backend.app.services.resume_parser import get_raw_resume
from backend.app.services.jd_matcher import simple_match_score

router = APIRouter(prefix="/qa")

@router.post("/generate", response_model=QAResponse)
def generate_qa(req: QARequest):
    # simple pipeline
    raw = get_raw_resume(req.resume_id)
    if not raw:
        raise HTTPException(status_code=404, detail="Resume not found.")
    questions = generate_questions_from_resume(req.resume_id, req.query)
    # compute a naive match score to include as a source
    score = simple_match_score(raw, req.query)
    answer = "Generated {} questions. Match score: {:.2f}".format(len(questions), score)
    # flatten as a single answer string and provide sources
    return QAResponse(answer=answer, sources=[f"match_score:{score}", "q_samples: " + " | ".join(questions[:3])])