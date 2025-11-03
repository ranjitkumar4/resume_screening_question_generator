import os
from dotenv import load_dotenv
from backend.core.llm_client import query_groq
from backend.core.prompts import resume_parse_prompt
from groq import Groq  # Import Groq client

# Load environment variables
load_dotenv()

#query_groq(client, prompt, model="llama-3.1-70b-versatile", max_tokens=512)

from backend.core.llm_client import query_groq
from backend.core.prompts import resume_parse_prompt

def extract_resume_info(resume_text):
    """
    Extract structured information (skills, experience, education, etc.)
    from a given resume text using Groq LLM.
    """
    try:
        # Get API key from .env
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            raise ValueError("GROQ_API_KEY not found in environment variables")

        # Initialize client
        client = Groq(api_key=api_key)

        # Build prompt
        prompt = resume_parse_prompt(resume_text)

        # Query the LLM
        result = query_groq(client=client, prompt=prompt, max_tokens=200)

        return result

    except Exception as e:
        print("Resume extraction failed:", e)
        return ""