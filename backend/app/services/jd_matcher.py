# Why: Implements FR-04 at a basic level.

from backend.app.utils.logger import get_logger

logger = get_logger("jd_matcher")

def simple_match_score(resume_text: str, jd_text: str) -> float:
    """
    Return a naive match score (0..1) based on shared keyword counts.
    """
    if not resume_text or not jd_text:
        return 0.0
    resume_words = set([w.strip(".,").lower() for w in resume_text.split()])
    jd_words = set([w.strip(".,").lower() for w in jd_text.split()])
    intersection = resume_words & jd_words
    score = len(intersection) / max(1, len(jd_words))
    logger.info("Match score computed: %s", score)
    return float(score)