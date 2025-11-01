# Why: Application entry point.

from fastapi import FastAPI
from backend.app.routes.health import router as health_router
from backend.app.routes.resume import router as resume_router
from backend.app.routes.qa import router as qa_router
from backend.app.utils.logger import get_logger

logger = get_logger("main")

app = FastAPI(title="Resume Agent", version="0.1.0")

# Include routers
app.include_router(health_router)
app.include_router(resume_router)
app.include_router(qa_router)

@app.on_event("startup")
def startup_event():
    logger.info("Starting Resume Agent API")