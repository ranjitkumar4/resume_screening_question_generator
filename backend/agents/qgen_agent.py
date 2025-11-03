from dotenv import load_dotenv
# Load environment variables
load_dotenv()

import json
import re
from backend.core.llm_client import query_groq
from backend.core.prompts import qgen_prompt
from backend.core.llm_client import get_groq_client


def clean_json_string(raw_text: str) -> str:
    """
    Clean up and extract JSON portion from model response.
    Handles extra text or formatting errors.
    """
    # Extract JSON portion using regex
    match = re.search(r"\{[\s\S]*\}", raw_text)
    if not match:
        return "{}"
    json_str = match.group(0)

    # Replace single quotes with double quotes
    json_str = json_str.replace("'", '"')

    # Remove trailing commas
    json_str = re.sub(r",\s*}", "}", json_str)
    json_str = re.sub(r",\s*]", "]", json_str)

    return json_str


def parse_questions_json(raw_text):
    """
    Parse JSON output from LLM with embedded quotes safely.
    Returns a dict with keys: technical, behavioral, general.
    """
    # Step 1: Clean escaped quotes
    cleaned_text = raw_text.replace('\\"', '"').replace('\“', '"').replace('\”', '"')

    # Step 2: Remove any trailing commas before closing brackets/braces
    cleaned_text = re.sub(r',(\s*[\]}])', r'\1', cleaned_text)

    # Step 3: Parse JSON safely
    try:
        questions = json.loads(cleaned_text)
    except json.JSONDecodeError as e:
        print(f"[WARN] JSON decode failed: {e}")
        # Fallback to empty categories
        questions = {"technical": [], "behavioral": [], "general": []}

    # Step 4: Ensure keys exist
    for key in ["technical", "behavioral", "general"]:
        questions.setdefault(key, [])

    return questions


def generate_questions(resume_info, jd_text):
    """
    Generate technical, behavioral, and general interview questions.
    """
    if not resume_info or not jd_text:
        return {"technical": [], "behavioral": [], "general": []}

    try:
        prompt = qgen_prompt(resume_info, jd_text)

        # ✅ Create client properly
        client = get_groq_client()
        if client is None:
            return {"technical": [], "behavioral": [], "general": []}

        # ✅ Query the LLM
        response = query_groq(client, prompt)
        raw_text = response if isinstance(response, str) else str(response)

        # --------------------------
        # Extract JSON from raw text
        # --------------------------
        match = re.search(r"\{.*\}", raw_text, flags=re.DOTALL)
        if match:
            json_str = match.group(0)
        else:
            print("[WARN] No JSON object found in LLM output.")
            questions = {"technical": [], "behavioral": [], "general": []}
            return questions

        # --------------------------
        # Fix common JSON issues
        # --------------------------
        # Remove trailing commas before } or ]
        json_str = re.sub(r",(\s*[}\]])", r"\1", json_str)

        # Replace smart quotes with normal quotes
        json_str = json_str.replace('“', '"').replace('”', '"').replace("‘", "'").replace("’", "'")

        # Escape unescaped double quotes inside strings
        # This finds quotes that are inside key/value strings and escapes them
        def escape_inner_quotes(match):
            s = match.group(0)
            s = re.sub(r'(?<!\\)"', r'\"', s)  # replace " with \" if not already escaped
            return s

        # Apply only inside string values (between quotes)
        json_str = re.sub(r'":\s*"([^"]*?)"', lambda m: '": "{}"'.format(m.group(1).replace('"', '\\"')), json_str)

        # --------------------------
        # Load JSON safely
        # --------------------------
        try:
            questions = json.loads(json_str)
            # print("questions here")
            # print(questions)
        except json.JSONDecodeError:
            print("[WARN] Invalid JSON from model, returning empty categories.")
            questions = {"technical": [], "behavioral": [], "general": []}

        # ✅ Ensure all keys exist
        for key in ["technical", "behavioral", "general"]:
            questions.setdefault(key, [])

        return questions

    except Exception as e:
        print(f"[QGEN ERROR]: {e}")
        return {"technical": [], "behavioral": [], "general": []}