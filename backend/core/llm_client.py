import os
from dotenv import load_dotenv
from groq import Groq

def get_groq_client():
    """
    Initialize and return Groq client using API key from .env.
    """
    try:
        # Load environment variables from .env file
        load_dotenv()

        # Fetch API key
        api_key = os.getenv("GROQ_API_KEY")

        if not api_key:
            raise ValueError("Missing GROQ_API_KEY in .env")

        # Initialize client
        client = Groq(api_key=api_key)
        return client

    except Exception as e:
        print(f"[ERROR] Groq client init failed: {e}")
        return None


def query_groq(client, prompt, model="llama-3.3-70b-versatile", max_tokens=512):
    """
    Send a chat completion request to Groq.
    """
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=max_tokens  # ✅ Groq uses max_output_tokens not max_tokens
        )
        return response.choices[0].message.content.strip()

    except Exception as e:
        print(f"Groq query failed: {e}")
        return ""