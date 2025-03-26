import os
import re
from google import genai
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=API_KEY)

def explain_topic(topic):
    prompt = (f"""
        Provide a detailed yet simplified explanation of the given topic. 
        If it is a theoretical concept, start with a definition and provide clear, concise details with examples where applicable. 
        If it is a code-related topic, include properly formatted code snippets with explanations. 
        Use a structured format with headings, bullet points, and step-by-step breakdowns.
        Ensure the explanation is easy to understand and removes any unnecessary complexity. 
        Here is the topic to explain:
        "{topic}"
    """)

    response = client.models.generate_content(
        model="gemini-2.0-flash-lite", contents=prompt
    )
    
    if not response or not response.text:
        return {"error": "Failed to generate explanation"}
    
    explanation = response.text
    return explanation

def markdown_to_plain_text(md_text: str) -> str:
    """
    Convert Markdown-styled text to plain text by removing common markdown syntax.
    """
    text = re.sub(r'#', '', md_text)
    text = re.sub(r'\*\*', '', text)
    text = re.sub(r'\*', '', text)
    text = re.sub(r'\n+', '\n', text)
    return text.strip()
