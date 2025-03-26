import re
import os
from google import genai
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=API_KEY)

def summarize_topic(text):
    prompt = (f"""
        Provide a detailed and well-structured Explanation for the text given below. 
        Start with the definition of the each topic (if applicable), providing concise but clear details.      
        After the definition, break down the important points in a structured list format, ensuring the summary is straightforward and easy to comprehend.   
        For shorter texts, provide at least 400 words of explanation, including details and context where necessary.
        For longer texts, extend the explanation to at least 800 words, ensuring depth and clarity.
        Conclude with a final statement that summarizes all the key points and ties together the topics of the text cohesively.        
        Here is the text to explain and summarize:
        "{text}"
    """)
    
    response = client.models.generate_content(
        model="gemini-2.0-flash-lite", contents=prompt
    )
    
    if not response or not response.text:
        return {"error": "Failed to generate summary"}
    
    summary = response.text
    return summary

def markdown_to_plain_text(md_text: str) -> str:
    """
    Convert Markdown-styled text to plain text by removing common markdown syntax.
    """
    text = re.sub(r'#', '', md_text)
    text = re.sub(r'\*\*', '', text)
    text = re.sub(r'\*', '', text)
    text = re.sub(r'\n+', '\n', text)
    return text.strip()
