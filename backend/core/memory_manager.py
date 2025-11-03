import json
from backend.core.file_utils import read_text_file
from langchain.memory import ConversationBufferMemory

MEMORY_FILE = "backend/data/memory_store.json"

def load_memory():
    try:
        with open(MEMORY_FILE, "r") as f:
            return json.load(f)
    except:
        return {}

def save_memory(memory):
    try:
        with open(MEMORY_FILE, "w") as f:
            json.dump(memory, f, indent=2)
    except Exception as e:
        print("Saving memory failed:", e)

def update_memory(candidate_name, parsed_resume, jd, questions, jd_score):
    """
    Update memory with a candidate evaluation.
    """
    try:
        memory = load_memory()
        memory[candidate_name] = {
            "parsed_resume": parsed_resume,
            "job_description": jd,
            "jd_score": jd_score,
            "questions": questions
        }
        save_memory(memory)
    except Exception as e:
        print(f"[MEMORY UPDATE ERROR]: {e}")

# For multi-turn conversation memory
conversation_memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

def add_to_memory(key, value):
    try:
        conversation_memory.save_context({"input": key}, {"output": value})
    except Exception as e:
        print("Memory update failed:", e)

def get_conversation_memory():
    return conversation_memory.load_memory_variables({})
