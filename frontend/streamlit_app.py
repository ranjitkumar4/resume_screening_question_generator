import streamlit as st
import requests
from pathlib import Path

API_BASE = st.secrets.get("API_BASE", "http://127.0.0.1:8000")

st.set_page_config(page_title="Resume Screening Agent")

st.title("Resume Screening & QGen Agent")

st.markdown("Upload a resume (text) — backend will parse and later generate interview questions.")

uploaded_file = st.file_uploader("Upload resume (txt)", type=["txt", "pdf", "docx"])
if uploaded_file:
    files = {"file": (uploaded_file.name, uploaded_file.getvalue())}
    resp = requests.post(f"{API_BASE}/resume/upload", files=files)
    if resp.status_code == 200:
        data = resp.json()
        st.success(f"Uploaded. Resume ID: {data['resume_id']}")
        st.text_area("Preview", value=data["preview"], height=200)
        st.session_state["resume_id"] = data["resume_id"]
    else:
        st.error(f"Upload failed: {resp.text}")

jd_text = st.text_area("Paste Job Description (for matching & question generation)", height=200)

if st.button("Generate Interview Questions"):
    resume_id = st.session_state.get("resume_id")
    if not resume_id:
        st.error("Upload a resume first.")
    else:
        resp = requests.post(f"{API_BASE}/qa/generate", json={"resume_id": resume_id, "query": jd_text})
        if resp.status_code == 200:
            out = resp.json()
            st.write("Answer:", out["answer"])
            st.write("Sources:", out["sources"])
        else:
            st.error("Generation failed: " + resp.text)