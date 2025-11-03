import streamlit as st
import requests
from io import BytesIO

# ---------------------------------------------------
# 🎨 Page Config
# ---------------------------------------------------
st.set_page_config(
    page_title="🤖 AI Resume Screening",
    page_icon="🧠",
    layout="wide"
)

# ---------------------------------------------------
# 🏷️ Header Section
# ---------------------------------------------------
st.title("🧠 AI Resume Screening & Interview Question Generator")
st.markdown(
    """
Welcome to the **AI-powered Resume Screening System**!  
Upload a candidate's resume and job description or paste the text directly to automatically:
- Parse key skills and experience
- Match candidate with JD
- Generate technical, behavioral, and general interview questions  
- Evaluate the quality of the generated questions using an evaluator agent
- Perform manual evaluation
"""
)
st.divider()

# ---------------------------------------------------
# 📂 Upload or Paste Section
# ---------------------------------------------------
st.header("📤 Upload Files or Paste Text")
col1, col2 = st.columns(2)

with col1:
    resume_file = st.file_uploader("📄 Upload Candidate Resume (.txt, .pdf, .docx)", type=["txt", "pdf", "docx"])
    resume_text_input = st.text_area("✏️ Or paste resume text here", placeholder="Paste candidate resume text...", height=200)

with col2:
    jd_file = st.file_uploader("💼 Upload Job Description (.txt, .pdf, .docx)", type=["txt", "pdf", "docx"])
    jd_text_input = st.text_area("✏️ Or paste JD text here", placeholder="Paste job description text...", height=200)

st.markdown("")
candidate_id = st.text_input("🆔 Candidate ID (optional)", value="candidate_1")
candidate_notes = st.text_area("🗒️ Notes (optional)", placeholder="Add recruiter notes, candidate remarks, etc.")
st.divider()

# ---------------------------------------------------
# 🚀 Workflow Buttons
# ---------------------------------------------------
col1, col2, col3 = st.columns(3)

# ------------------- 1️⃣ Run Screening Workflow -------------------
with col1:
    st.markdown("### 🚀 Run Screening Workflow")
    if st.button("▶️ Start Workflow"):
        if (resume_file or resume_text_input) and (jd_file or jd_text_input):
            with st.spinner("Running AI Screening Workflow... ⏳"):
                try:
                    if resume_file and jd_file:
                        files = {
                            "resume_file": (resume_file.name, BytesIO(resume_file.getvalue())),
                            "jd_file": (jd_file.name, BytesIO(jd_file.getvalue()))
                        }
                        res = requests.post("http://127.0.0.1:8000/supervisor_workflow_files/", files=files)
                    else:
                        payload = {
                            "resume_text": resume_text_input,
                            "jd_text": jd_text_input
                        }
                        res = requests.post("http://127.0.0.1:8000/supervisor_workflow_text/", json=payload)

                    if res.status_code == 200:
                        workflow_result = res.json()
                        st.session_state['workflow_result'] = workflow_result
                        st.success("✅ Workflow completed successfully!")

                        st.subheader("🧾 Parsed Resume Summary")
                        st.text_area("Extracted Resume Info", workflow_result.get("parsed_resume", ""), height=180)

                        st.subheader("📊 JD Match Results")
                        st.json(workflow_result.get("jd_match", {}))
                    else:
                        st.error(f"❌ Error: {res.status_code} - {res.text}")
                except Exception as e:
                    st.error(f"⚠️ Backend request failed: {str(e)}")
        else:
            st.warning("📌 Please upload or paste both resume and job description before running workflow.")

# ------------------- 2️⃣ Generate Interview Questions -------------------
with col2:
    st.markdown("### ❓ Generate Interview Questions")
    if st.button("📝 Generate Questions"):
        if (resume_file or resume_text_input) and (jd_file or jd_text_input):
            with st.spinner("Generating Questions... 🧠"):
                try:
                    if resume_file and jd_file:
                        files = {
                            "resume_file": (resume_file.name, BytesIO(resume_file.getvalue())),
                            "jd_file": (jd_file.name, BytesIO(jd_file.getvalue()))
                        }
                        res = requests.post("http://127.0.0.1:8000/generate_questions/", files=files)
                    else:
                        payload = {
                            "resume_text": resume_text_input,
                            "jd_text": jd_text_input
                        }
                        res = requests.post("http://127.0.0.1:8000/generate_questions_text/", json=payload)

                    if res.status_code == 200:
                        questions = res.json()
                        st.session_state['questions'] = questions
                        st.success("✅ Questions generated successfully!")

                        st.markdown("### 🎯 Technical Questions")
                        for q in questions.get("technical", []):
                            st.markdown(f"- {q}")

                        st.markdown("### 💬 Behavioral Questions")
                        for q in questions.get("behavioral", []):
                            st.markdown(f"- {q}")

                        st.markdown("### 🧠 General Questions")
                        for q in questions.get("general", []):
                            st.markdown(f"- {q}")
                    else:
                        st.error(f"❌ Error: {res.status_code} - {res.text}")
                except Exception as e:
                    st.error(f"⚠️ Backend request failed: {str(e)}")
        else:
            st.warning("📌 Please upload or paste both resume and job description before generating questions.")

# ------------------- 3️⃣ Evaluator Agent -------------------
with col3:
    st.markdown("### 🏆 Evaluator Agent")
    if st.button("🧾 Evaluate Questions"):
        if (resume_file or resume_text_input) and (jd_file or jd_text_input):
            with st.spinner("Evaluating Generated Questions... 🔍"):
                try:
                    if resume_file and jd_file:
                        files = {
                            "resume_file": (resume_file.name, BytesIO(resume_file.getvalue())),
                            "jd_file": (jd_file.name, BytesIO(jd_file.getvalue()))
                        }
                        res = requests.post("http://127.0.0.1:8000/evaluate_candidate_files/", files=files)
                    else:
                        payload = {
                            "resume_text": resume_text_input,
                            "jd_text": jd_text_input
                        }
                        res = requests.post("http://127.0.0.1:8000/evaluate_candidate_text/", json=payload)

                    if res.status_code == 200:
                        evaluation = res.json()
                        st.success("✅ Evaluation completed!")

                        st.subheader("📋 Evaluation / Critique")
                        st.json(evaluation)
                    else:
                        st.error(f"❌ Error: {res.status_code} - {res.text}")
                except Exception as e:
                    st.error(f"⚠️ Backend request failed: {str(e)}")
        else:
            st.warning("📌 Please upload or paste both resume and job description before evaluating.")
# ------------------- 4️⃣ Manual Evaluation -------------------
st.divider()
st.subheader("📝 Manual Evaluation of Agent Outputs")
if 'workflow_result' in st.session_state and 'questions' in st.session_state:
    workflow_result = st.session_state['workflow_result']
    questions = st.session_state['questions']
    
    with st.form("manual_eval_form"):
        parsed_accuracy = st.slider("Parsed Resume Accuracy", 1, 5, 3)
        jd_match_relevance = st.slider("JD Match Relevance", 1, 5, 3)
        question_quality = st.slider("Question Quality", 1, 5, 3)
        submit_eval = st.form_submit_button("Submit Manual Evaluation")

        if submit_eval:
            manual_payload = {
                "resume_name": resume_file.name if resume_file else "pasted_resume",
                "jd_name": jd_file.name if jd_file else "pasted_jd",
                "parsed_resume": workflow_result.get("parsed_resume", ""),
                "jd_match_summary": workflow_result.get("jd_match", {}),
                "questions": questions,
                "human_ratings": {
                    "parsed_accuracy": parsed_accuracy,
                    "jd_match_relevance": jd_match_relevance,
                    "question_quality": question_quality
                }
            }
            st.success("✅ Manual evaluation recorded!")
            st.json(manual_payload)
else:
    st.info("ℹ️ Please run workflow and generate questions first to perform manual evaluation.")

# ---------------------------------------------------
# 💡 Tips & Notes Section
# ---------------------------------------------------
st.divider()
st.header("💡 Tips & Notes")
st.markdown(
    """
- 🧾 **Supported formats:** `.txt`, `.pdf`, `.docx`  
- ✏️ You can also paste resume and JD text directly  
- 🧍 **Candidate ID** helps track candidates in memory  
- ⚙️ **Ensure FastAPI backend** is running at: `http://127.0.0.1:8000/`  
- 🗒️ Use notes to add recruiter context or special instructions  
- 🤖 The AI model generates:
  - **5 Technical Questions**
  - **5 Behavioral Questions**
  - **3 General Questions**
- 🏆 The Evaluator Agent reviews the questions, provides critique, and suggests improvements
- 📝 Manual evaluation allows human reviewers to rate parsed info, JD match, and question quality
"""
)
st.caption("Built with ❤️ using Streamlit + FastAPI + GPT-powered Agents")