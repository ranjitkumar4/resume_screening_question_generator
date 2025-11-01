from app.services.qgen import generate_questions
from sentence_transformers import SentenceTransformer, util

model = SentenceTransformer("all-MiniLM-L6-v2")

questions = generate_questions("data scientist")
embeddings = model.encode(questions)
similarity = util.cos_sim(embeddings, embeddings)

# Lower mean similarity → higher diversity
import numpy as np
mean_sim = np.mean(similarity.numpy()[np.triu_indices(len(questions), k=1)])
diversity = (1 - mean_sim) * 100

print(f"Question Diversity: {diversity:.2f}%")
assert diversity > 70