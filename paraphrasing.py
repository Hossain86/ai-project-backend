import os
from google import genai
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=API_KEY)

def paraphrase_text(text):
    """
    Uses Gemini AI to paraphrase the given text while keeping its original meaning.
    """
    prompt = (f"""
        Paraphrase the following text while keeping the meaning intact. Ensure that the rewritten version:
        - Uses different wording and sentence structures.
        - Avoids excessive repetition.
        - Maintains clarity and coherence.
        
        Original text:
        "{text}"
    """)

    response = client.models.generate_content(
        model="gemini-2.0-flash-lite", contents=prompt
    )

    if not response or not response.text:
        return {"error": "Failed to paraphrase text"}

    return response.text
