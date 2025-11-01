"""
Creates the folder and file structure for Resume Screening Question Generator project.
Run this once inside your cloned GitHub repository.
"""

import os

BASE_DIR = os.getcwd()

folders = [
    "backend/app/routes",
    "backend/app/services",
    "backend/app/utils",
    "frontend/assets"
]

files = {
    "backend/app/__init__.py": "",
    "backend/app/main.py": "",
    "backend/app/settings.py": "",
    "backend/app/schemas.py": "",
    "backend/app/routes/__init__.py": "",
    "backend/app/routes/health.py": "",
    "backend/app/routes/resume.py": "",
    "backend/app/routes/qa.py": "",
    "backend/app/services/__init__.py": "",
    "backend/app/services/llm.py": "",
    "backend/app/services/resume_parser.py": "",
    "backend/app/services/jd_matcher.py": "",
    "backend/app/services/qgen.py": "",
    "backend/app/services/memory_store.py": "",
    "backend/app/utils/__init__.py": "",
    "backend/app/utils/logger.py": "",
    "backend/requirements.txt": "",
    "backend/.env_example": "",
    "frontend/streamlit_app.py": ""
}

for folder in folders:
    os.makedirs(os.path.join(BASE_DIR, folder), exist_ok=True)

for path, content in files.items():
    full_path = os.path.join(BASE_DIR, path)
    with open(full_path, "w", encoding="utf-8") as f:
        f.write(content)

print(f"✅ Project structure created successfully under: {BASE_DIR}")