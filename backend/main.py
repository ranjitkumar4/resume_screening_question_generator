from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from io import BytesIO
from backend.core.file_utils import read_text_file, extract_text_from_file
from backend.agents.supervisor_agent import run_supervisor
from backend.agents.evaluator_agent import evaluate_candidate
from backend.agents.qgen_agent import generate_questions
from backend.agents.evaluator_agent import evaluate_questions

app = FastAPI(
    title="Resume Intelligence Agent API",
    description="Handles resume parsing, JD matching, question generation, and candidate evaluation.",
    version="1.0.0",
)

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

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# --------------------------
# Request model for text input
# --------------------------
class TextInput(BaseModel):
    resume_text: str
    jd_text: str

# -----------------------------
# 1️⃣ SUPERVISOR WORKFLOW (FILES)
# -----------------------------
@app.post("/supervisor_workflow_files/")
async def supervisor_workflow_files(
    resume_file: UploadFile = File(...),
    jd_file: UploadFile = File(...),
):
    """
    Upload resume and JD files → Extract → Match → Generate Questions.
    """
    try:
        # Save temporary files
        resume_path = f"temp_resume_{resume_file.filename}"
        jd_path = f"temp_jd_{jd_file.filename}"

        with open(resume_path, "wb") as f:
            f.write(await resume_file.read())
        with open(jd_path, "wb") as f:
            f.write(await jd_file.read())

        # Read extracted text
        resume_text = read_text_file(resume_path)
        jd_text = read_text_file(jd_path)

        result = run_supervisor(resume_text, jd_text)
        return result

    except Exception as e:
        print(f"[SUPERVISOR ERROR]: {e}")
        return {"error": str(e)}

# -----------------------------
# 1️⃣ SUPERVISOR WORKFLOW (TEXT)
# -----------------------------
@app.post("/supervisor_workflow_text/")
async def supervisor_workflow_text(payload: TextInput):
    """
    Run workflow using pasted text for resume and JD → Parse → Match → Generate Questions.
    """
    try:
        result = run_supervisor(payload.resume_text, payload.jd_text)
        return result
    except Exception as e:
        print(f"[SUPERVISOR ERROR]: {e}")
        return {"error": str(e)}

# -----------------------------
# 2️⃣ EVALUATION (FILES)
# -----------------------------
@app.post("/evaluate_candidate_files/")
async def evaluate_candidate_files(
    resume_file: UploadFile = File(...),
    jd_file: UploadFile = File(...),
):
    """
    Upload resume + JD → Generate questions → Evaluate questions.
    """
    try:
        resume_path = f"temp_resume_{resume_file.filename}"
        jd_path = f"temp_jd_{jd_file.filename}"

        with open(resume_path, "wb") as f:
            f.write(await resume_file.read())
        with open(jd_path, "wb") as f:
            f.write(await jd_file.read())

        resume_text = read_text_file(resume_path)
        jd_text = read_text_file(jd_path)

        eval_result = evaluate_candidate(resume_text, jd_text)
        return eval_result

    except Exception as e:
        print(f"[EVALUATOR ERROR]: {e}")
        return {"error": str(e)}


# -----------------------------
# 2️⃣ EVALUATION (TEXT)
# -----------------------------
@app.post("/evaluate_candidate_text/")
async def evaluate_candidate_text(payload: TextInput):
    """
    Evaluate candidate using pasted resume and JD text.
    """
    try:
        eval_result = evaluate_candidate(payload.resume_text, payload.jd_text)
        return eval_result
    except Exception as e:
        print(f"[EVALUATOR ERROR]: {e}")
        return {"error": str(e)}

# -----------------------------
# 3️⃣ QUESTION GENERATION (FILES)
# -----------------------------
@app.post("/generate_questions/")
async def generate_questions_endpoint(
    resume_file: UploadFile = File(...),
    jd_file: UploadFile = File(...),
):
    """
    Upload resume + JD → Generate Technical, Behavioral, and General Questions.
    """
    try:
        resume_content = await resume_file.read()
        jd_content = await jd_file.read()

        resume_text = resume_content.decode("utf-8", errors="ignore")
        jd_text = jd_content.decode("utf-8", errors="ignore")

        result = generate_questions(resume_text, jd_text)
        return result

    except Exception as e:
        print(f"[QUESTION GENERATION ERROR]: {e}")
        return {"error": str(e)}

# -----------------------------
# 3️⃣ QUESTION GENERATION (TEXT)
# -----------------------------
@app.post("/generate_questions_text/")
async def generate_questions_text(payload: TextInput):
    """
    Generate technical, behavioral, and general questions using pasted text.
    """
    try:
        questions = generate_questions(payload.resume_text, payload.jd_text)
        return questions
    except Exception as e:
        print(f"[QUESTION GENERATION ERROR]: {e}")
        return {"technical": [], "behavioral": [], "general": [], "error": str(e)}

from backend.agents.manual_eval import submit_manual_evaluation, list_manual_evaluations
from pydantic import BaseModel
from typing import Dict

class ManualEvalInput(BaseModel):
    resume_name: str
    jd_name: str
    parsed_resume: str
    jd_match_summary: Dict
    questions: Dict
    human_ratings: Dict  # keys: parsed_accuracy, jd_match_relevance, question_quality

# -----------------------------
# 4️⃣ MANUAL EVALUATION SUBMIT
# -----------------------------
@app.post("/manual_evaluation/")
async def manual_evaluation(payload: ManualEvalInput):
    """
    Submit manual evaluation for a candidate + JD + agent outputs.
    """
    try:
        result = submit_manual_evaluation(
            resume_name=payload.resume_name,
            jd_name=payload.jd_name,
            parsed_resume=payload.parsed_resume,
            jd_match_summary=payload.jd_match_summary,
            questions=payload.questions,
            human_ratings=payload.human_ratings
        )
        return result
    except Exception as e:
        print(f"[MANUAL EVAL ERROR]: {e}")
        return {"error": str(e)}


# -----------------------------
# 5️⃣ LIST MANUAL EVALUATIONS
# -----------------------------
@app.get("/manual_evaluations/")
async def get_manual_evaluations():
    """
    List all manual evaluations submitted so far.
    """
    try:
        return list_manual_evaluations()
    except Exception as e:
        print(f"[MANUAL EVAL ERROR]: {e}")
        return {"error": str(e)}