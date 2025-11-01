
## Why: Central LLM wrapper so other services reuse the same client and configuration. (BRD: LLM provider integration)

from typing import Dict, Any
from constants import GROQ_MODEL_DEFAULT, GROQ_TEMPERATURE_DEFAULT
from backend.app.settings import get_settings
from backend.app.utils.logger import get_logger

logger = get_logger("llm")
settings = get_settings()

# Import Groq LLM wrapper. If your environment uses a direct `groq` client, adjust accordingly.
try:
    from langchain_groq import ChatGroq
except Exception:
    # If you don't have langchain_groq, use a lightweight fallback that raises an error
    ChatGroq = None

def init_groq_client():
    """
    Initialize and return a Groq Chat client configured from environment.
    Returns:
        ChatGroq or raises RuntimeError if client not available
    """
    api_key = settings.GROQ_API_KEY
    model_name = settings.GROQ_MODEL or GROQ_MODEL_DEFAULT
    temperature = settings.GROQ_TEMPERATURE or GROQ_TEMPERATURE_DEFAULT

    if ChatGroq is None:
        raise RuntimeError("ChatGroq client not installed. Install langchain_groq or adapt this function.")
    client = ChatGroq(api_key=api_key, model_name=model_name, temperature=temperature)
    logger.info("Initialized Groq client with model=%s", model_name)
    return client

def classify_sentiment_via_prompt(client, prompt: str, temperature: float = 0.0) -> str:
    """
    Send a chat completion request to the Groq client.

    Args:
        client: Groq client instance
        prompt: User prompt (string)
        temperature: float, sampling temperature

    Returns:
        text response (str)
    """
    # Basic wrapper - the client API may differ; adjust fields to your client
    resp = client.chat.completions.create(
        model=client.model_name,
        messages=[{"role":"user", "content": prompt}],
        temperature=temperature
    )
    # Extract string (adjust according to your client response)
    try:
        return resp.choices[0].message.content
    except Exception as e:
        logger.exception("Failed to parse Groq response: %s", e)
        raise