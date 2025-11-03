from backend.core.embeddings_utils import compute_similarity

def match_resume_to_jd(resume_text, jd_text):
    try:
        score = compute_similarity(resume_text, jd_text)
        summary = f"Candidate match score: {score*100}%"
        return {"score": score, "summary": summary}
    except Exception as e:
        print("JD matching failed:", e)
        return {"score": 0, "summary": ""}


from backend.core.llm_client import get_groq_client
from backend.core.prompts import jd_match_prompt
import json

def match_jd(resume_info, jd_text):
    """
    Generate relevance score and summary between resume and JD.
    Returns:
        {
            "score": 0-100,
            "summary": "..."
        }
    """
    try:
        client = get_groq_client()
        if client is None:
            raise ValueError("Groq client not initialized.")

        # Prepare prompt with JSON instructions
        prompt = jd_match_prompt(resume_info, jd_text)
        prompt += (
            "\n\nPlease respond in strict JSON format:\n"
            "{\n"
            '  "score": 0-100,\n'
            '  "summary": "..." \n'
            "}"
        )

        response = client.chat(prompt)

        # Parse JSON safely
        try:
            result = json.loads(response.text)
            score = result.get("score", 0)
            summary = result.get("summary", "")
        except json.JSONDecodeError:
            print("[JD MATCHING ERROR]: Failed to parse JSON response")
            score, summary = 0, ""

        return {"score": score, "summary": summary}

    except Exception as e:
        print(f"[JD MATCHING ERROR]: {e}")
        return {"score": 0, "summary": ""}