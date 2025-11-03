# backend/agents/evaluate.py
import json
from backend.core.llm_client import get_groq_client

def evaluate_questions(resume_info: str, jd_text: str, questions: dict, model = "llama-3.3-70b-versatile"):
    """
    Evaluate generated interview questions using LLM.
    Returns ratings (1-5) and critique for each question.
    """
    if not resume_info or not jd_text or not questions:
        return {"ratings": {}, "critique": "Missing input data"}

    try:
        client = get_groq_client()
        if client is None:
            return {"ratings": {}, "critique": "LLM client not available"}

        # Build evaluation prompt
        eval_prompt = (
            f"Candidate information:\n{resume_info}\n\n"
            f"Job description:\n{jd_text}\n\n"
            f"Generated questions:\n{json.dumps(questions, indent=2)}\n\n"
            "Please evaluate each question for relevance, clarity, and quality (scale 1-5), "
            "and provide a short critique or improvement suggestion for each. "
            "Return the result as a JSON object with keys 'technical', 'behavioral', 'general', "
            "each containing a list of {'question', 'rating', 'critique'}."
        )

        # ✅ Call the LLM
        response = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": eval_prompt}],
            max_tokens=512
        )

        # Extract content safely
        content = ""
        if response and getattr(response, "choices", None):
            content = response.choices[0].message.content.strip()

        # Attempt to parse JSON
        try:
            evaluation = json.loads(content)
        except json.JSONDecodeError:
            # Fallback: return raw content
            evaluation = {"ratings": {}, "critique": content}

        return evaluation

    except Exception as e:
        print(f"[EVALUATOR ERROR]: {e}")
        return {"ratings": {}, "critique": str(e)}

from backend.agents.qgen_agent import generate_questions
from backend.agents.evaluator_agent import evaluate_questions

def evaluate_candidate(resume_text: str, jd_text: str):
    """
    Full evaluation pipeline:
    1. Generate questions from resume + JD
    2. Evaluate those questions using Evaluator Agent
    """
    # Step 1: Generate questions
    questions = generate_questions(resume_text, jd_text)

    # Step 2: Evaluate the questions
    evaluation = evaluate_questions(resume_text, jd_text, questions)

    # Include the questions in the response for context
    return {
        "questions": questions,
        "evaluation": evaluation
    }