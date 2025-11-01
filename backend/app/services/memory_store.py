# Why: FR-07 (memory support).

import json, os
from typing import Dict, Any
from backend.app.utils.logger import get_logger

logger = get_logger("memory_store")
MEMORY_FILE = "backend/memory_store.json"

def save_memory(key: str, value: Any):
    d = {}
    if os.path.exists(MEMORY_FILE):
        try:
            d = json.load(open(MEMORY_FILE, "r", encoding="utf-8"))
        except Exception:
            d = {}
    d[key] = value
    json.dump(d, open(MEMORY_FILE, "w", encoding="utf-8"), indent=2)
    logger.info("Saved memory key=%s", key)

def load_memory(key: str):
    if not os.path.exists(MEMORY_FILE):
        return None
    d = json.load(open(MEMORY_FILE, "r", encoding="utf-8"))
    return d.get(key)