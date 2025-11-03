import os

# Base folder
base_folder = "resume_interview_agent"

# Folder structure
folders = [
    "backend/agents",
    "backend/core",
    "backend/config",
    "backend/data/resumes",
    "backend/data/jds",
    "frontend/pages"
]

# Files to create
files = [
    "backend/agents/resume_extractor_agent.py",
    "backend/agents/jd_matcher_agent.py",
    "backend/agents/qgen_agent.py",
    "backend/agents/evaluator_agent.py",
    "backend/agents/tool_rag_agent.py",
    "backend/core/llm_client.py",
    "backend/core/file_utils.py",
    "backend/core/embeddings_utils.py",
    "backend/core/prompts.py",
    "backend/core/memory_manager.py",
    "backend/config/settings.py",
    "backend/data/resumes/resume1.txt",
    "backend/data/resumes/resume2.txt",
    "backend/data/jds/jd1.txt",
    "backend/data/jds/jd2.txt",
    "backend/data/memory_store.json",
    "backend/main.py",
    "frontend/streamlit_app.py",
    "folder_structure.py",
    "README.md",
    ".env_example",
    "requirements.txt"
]

# Create folders
for folder in folders:
    path = os.path.join(base_folder, folder)
    os.makedirs(path, exist_ok=True)
    print(f"Created folder: {path}")

# Create empty files
for file in files:
    path = os.path.join(base_folder, file)
    if not os.path.exists(path):
        with open(path, "w", encoding="utf-8") as f:
            if path.endswith(".json"):
                f.write("{}")  # empty JSON for memory_store
            else:
                f.write("")  # empty file
        print(f"Created file: {path}")
    else:
        print(f"File already exists: {path}")

print("\n✅ Folder structure and files created successfully!")