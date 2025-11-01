from app.services.jd_matcher import match_resume_to_jd
from sklearn.metrics.pairwise import cosine_similarity

scores = []
# Sample resumes and JDs
test_pairs = [
    ("data_scientist_resume.pdf", "data_scientist_jd.txt"),
    ("ml_engineer_resume.pdf", "ml_engineer_jd.txt"),
]

for res, jd in test_pairs:
    score = match_resume_to_jd(res, jd)
    scores.append(score)

avg_score = sum(scores) / len(scores)
print(f"JD Match Relevance: {avg_score * 100:.2f}%")
assert avg_score * 100 >= 85