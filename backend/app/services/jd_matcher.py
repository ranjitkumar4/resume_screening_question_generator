# Why: Implements FR-04 at a basic level.

# from backend.app.utils.logger import get_logger

# logger = get_logger("jd_matcher")

# def simple_match_score(resume_text: str, jd_text: str) -> float:
#     """
#     Return a naive match score (0..1) based on shared keyword counts.
#     """
#     if not resume_text or not jd_text:
#         return 0.0
#     resume_words = set([w.strip(".,").lower() for w in resume_text.split()])
#     jd_words = set([w.strip(".,").lower() for w in jd_text.split()])
#     intersection = resume_words & jd_words
#     score = len(intersection) / max(1, len(jd_words))
#     logger.info("Match score computed: %s", score)
#     return float(score)

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import re

def clean_text(text: str) -> str:
    """Normalize text by lowering case and removing non-alphanumeric characters."""
    text = text.lower()
    text = re.sub(r"[^a-z0-9\s]", " ", text)
    return text

def compute_jd_match_score(resume_text: str, jd_text: str) -> float:
    """
    Compute semantic similarity between resume and job description.
    Returns a score between 0 and 1.
    """
    resume_text = clean_text(resume_text)
    jd_text = clean_text(jd_text)

    if not resume_text.strip() or not jd_text.strip():
        return 0.0

    vectorizer = TfidfVectorizer(stop_words="english")
    vectors = vectorizer.fit_transform([resume_text, jd_text])
    similarity = cosine_similarity(vectors[0:1], vectors[1:2])
    return round(float(similarity[0][0]), 3)
