# backend/agents/manual_eval.py
from typing import List, Dict

# Store evaluations in memory (can be later extended to DB)
manual_evaluations = []

def submit_manual_evaluation(
    resume_name: str,
    jd_name: str,
    parsed_resume: str,
    jd_match_summary: Dict,
    questions: Dict,
    human_ratings: Dict
):
    """
    Store manual evaluation for a given resume + JD + agent outputs.
    
    human_ratings example:
    {
        "parsed_accuracy": 4,
        "jd_match_relevance": 5,
        "question_quality": 3
    }
    """
    eval_record = {
        "resume_name": resume_name,
        "jd_name": jd_name,
        "parsed_resume": parsed_resume,
        "jd_match_summary": jd_match_summary,
        "questions": questions,
        "human_ratings": human_ratings
    }
    manual_evaluations.append(eval_record)
    return {"status": "success", "record_id": len(manual_evaluations)-1}


def list_manual_evaluations():
    """Return all manual evaluation records"""
    return manual_evaluations