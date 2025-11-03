from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def compute_similarity(text1, text2):
    try:
        if isinstance(text1, (dict, list)):
            text1 = str(text1)
        if isinstance(text2, (dict, list)):
            text2 = str(text2)

        text1 = text1.lower()
        text2 = text2.lower()

        # Example dummy similarity if embeddings aren't implemented
        if not text1 or not text2:
            return 0.0

        # Replace below with actual cosine similarity
        similarity = len(set(text1.split()) & set(text2.split())) / max(len(set(text1.split())), 1)
        return round(similarity, 3)

    except Exception as e:
        print("Similarity computation failed:", e)
        return 0.0