# resume_screening_question_generator
An end-to-end GenAI system built using FastAPI, Streamlit, and Groq LLM, designed to automate resume screening, match candidates with job descriptions (JDs), and generate personalized interview questions — both technical and behavioral.

# Resume Screening & Interview QGen Capstone

## Project purpose
Build a resume screening + interview question generation system using FastAPI backend, Streamlit frontend, and Groq LLM integration.

## Local setup (backend)
1. cd backend
2. python -m venv .venv
3. .\.venv\Scripts\activate  (Windows) or source .venv/bin/activate (mac/linux)
4. pip install -r requirements.txt
5. Copy `.env_example` -> `.env` and set GROQ_API_KEY value
6. uvicorn backend.app.main:app --reload

## Frontend (Streamlit)
1. cd frontend
2. streamlit run streamlit_app.py

## Notes
- Do not commit `.env`. Keep secrets local.
- This repository contains starter stubs (replace logic with LLM calls in services/llm.py).