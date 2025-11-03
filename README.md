# 🤖 AI Resume Screening & Interview Question Generation Assistant

## Project Overview

This repository contains a **full-stack AI application** that helps HR and recruitment teams automate:

- Resume parsing
- Matching candidates to job descriptions
- Generating **personalized technical and behavioral interview questions**
- Providing **JD match scores** and summaries
- Maintaining **memory across evaluations**
- Evaluating the quality of generated questions via an **LLM evaluator agent**

The system uses **FastAPI** for backend APIs, **Streamlit** for a dynamic frontend, and **Groq LLM (`llama-3.3-70b-versatile`)** for AI reasoning.

---

## Folder Structure



---

## Setup Instructions

1. **Clone the repository**

```bash
git clone <repo_url>
cd resume_interview_agent

cp .env_example .env
# Edit .env and add your keys
GROQ_API_KEY="your_real_groq_api_key"
GROQ_MODEL_NAME="llama-3.3-70b-versatile"

pip install -r requirements.txt
uvicorn backend.main:app --reload
streamlit run frontend/streamlit_app.py

How to Use the App
Upload a resume (TXT format)
Upload a job description (TXT format)
Click Generate Results

View:
Parsed Resume Information
JD Match Score & Summary
Generated Technical & Behavioral Questions
LLM Evaluation / Critique
Stored Memory of evaluations

# resume_interview_agent/
# ├── backend/
# │   ├── agents/                     # Modular agent scripts
# │   │   ├── resume_extractor_agent.py   # Parses resumes (FR-02)
# │   │   ├── jd_matcher_agent.py         # Matches resume vs JD (FR-04)
# │   │   ├── qgen_agent.py               # Generates technical & behavioral questions (FR-05/06)
# │   │   ├── evaluator_agent.py          # Evaluates agent outputs (manual/LLM/agent)
# │   │   └── tool_rag_agent.py           # Optional tool / RAG integration (FR-08)
# │   ├── core/                       # Core utilities used by agents
# │   │   ├── llm_client.py                # LLM API wrapper
# │   │   ├── file_utils.py                # Resume/JD file reading & parsing
# │   │   ├── embeddings_utils.py          # Semantic similarity & embeddings
# │   │   ├── prompts.py                   # Centralized prompts for LLM calls
# │   │   └── memory_manager.py            # Context/memory management (FR-07)
# │   ├── config/                     # FastAPI configuration & environment
# │   │   └── settings.py                  # Pydantic BaseSettings, loads .env
# │   ├── data/                       # Sample/resume, JD, memory storage
# │   │   ├── resumes/
# │   │   │   ├── resume1.txt
# │   │   │   └── resume2.txt
# │   │   ├── jds/
# │   │   │   ├── jd1.txt
# │   │   │   └── jd2.txt
# │   │   └── memory_store.json            # Persistent or mock memory
# │   ├── main.py                     # FastAPI backend entry point / agent orchestration
# │   └── tests/                      # Unit / integration tests for agents & utils
# ├── frontend/
# │   ├── streamlit_app.py            # Main Streamlit UI
# │   ├── pages/                      # Optional multipage UI for modular screens
# │   └── assets/                     # Optional images/icons for UI
# ├── evaluation_reports/             # Stores manual/LLM evaluation outputs (Markdown/CSV)
# ├── notebooks/                      # Optional notebooks for experimentation / analysis
# ├── logs/                           # Optional runtime logs, API calls, or memory changes
# ├── .env_example                    # Example environment variables (submit only this)
# ├── pyproject.toml                  # UV dependency management (replaces requirements.txt)
# ├── folder_structure.py             # Script to generate folders/files automatically
# └── README.md                       # Setup, instructions, project documentation