import re
import os
from google import genai
from dotenv import load_dotenv
load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")
client=genai.Client(api_key=API_KEY)
def assignment_gen(text):
    prompt = (f"""
        Generate a detailed and well-structured lab report on "{text}". The report should include the following sections:
        1. Title: Create a suitable and concise title for the lab report based on "{text}".
        2. Introduction (150-200 words): Explain the background and theory behind "{text}" in simple and clear terms. Provide enough context so that even a beginner can understand its importance.
        3. Procedure / Code (C++ if coding-related and for assembly code use assembly language):
            If the topic is related to an experiment, describe the step-by-step procedure in a clear and structured way.
            If the topic involves coding, provide a well-optimized C++ implementation that follows best practices.
        4. Results: Show the output from the experiment or the execution of the code, ensuring clarity and correctness.
        5. Analysis & Discussion: Explain the meaning of the results, compare them with expected outcomes, and discuss any interesting observations.
        6. Conclusion (150-200 words): Summarize the key findings, lessons learned from "{text}".
        The final lab report should be clear, structured, and easy to understand for anyone reading it."""
      )
    response = client.models.generate_content(
        model="gemini-2.0-flash-lite", contents=prompt
    )
    if not response or not response.text:
      return {"error ":"Failed to generate Lab Report"}
    lab_report = response.text
    return lab_report
def markdown_to_plain_text(md_text: str) -> str:
    """
    A simple conversion that removes common markdown syntax. 
    (For more robust conversion, consider using libraries such as 'markdown' + 'BeautifulSoup'.)
    """
    text = re.sub(r'#', '', md_text)
    text = re.sub(r'\*\*', '', text)
    text = re.sub(r'\*', '', text)
    text = re.sub(r'\n+', '\n', text)
    return text.strip()