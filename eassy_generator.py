import re
import os
from google import genai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=API_KEY)

def generate_essay_or_paragraph(topic: str, essay_type: str):
    """Generate a structured essay or paragraph based on the given topic."""
    
    # Determine the prompt based on the essay type (essay or paragraph)
    prompt = (f"""
        Write a well-structured {essay_type} on the topic: "{topic}". 
        - Ensure clarity, coherence, and logical flow.
        - Use simple yet informative language.
        - Provide relevant details but avoid unnecessary filler text.
    """)
    
    try:
        # Generate content using the Gemini API
        response = client.models.generate_content(
            model="gemini-2.0-flash", contents=prompt
        )
        
        # Check if the response contains text
        if not response or not response.text:
            return {"error": "Failed to generate essay/paragraph"}
        
        return {"essay": response.text}
    
    except Exception as e:
        return {"error": str(e)}

