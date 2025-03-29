import re
import os
from google import genai
from dotenv import load_dotenv
load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=API_KEY)

def generateMCQ(text, num_questions, level, difficulty):
    """Generate multiple-choice questions (MCQs) from extracted text."""
    prompt = (
        f"""
            Generate {num_questions} multiple-choice questions (MCQs) from the text below.
            Difficulty: {difficulty}. Education Level: {level}.
            Ensure four options per question. Format:
            1. What is AI?
            a) A fruit
            b) A technology
            c) A planet
            d) A language
            Answer: b) A technology
            Text:
            {text}
            """
    )

    response = client.models.generate_content(
        model="gemini-2.0-flash", contents=prompt
    )
    if not response or not response.text:
        return {"error": "Failed to generate MCQs."}

    mcq_text = response.text
    pattern = re.compile(r'(\d+): (.*?)\n\s*a\) (.*?)\n\s*b\) (.*?)\n\s*c\) (.*?)\n\s*d\) (.*?)\nAnswer: (.*?)\n', re.DOTALL)
    mcqs = []

    for match in pattern.finditer(mcq_text):
        mcqs.append({
            "question": match.group(2).strip(),
            "options": [
                {"label": "a", "text": match.group(3).strip()},
                {"label": "b", "text": match.group(4).strip()},
                {"label": "c", "text": match.group(5).strip()},
                {"label": "d", "text": match.group(6).strip()},
            ],
            "answer": match.group(7).strip()
        })

    return mcqs
