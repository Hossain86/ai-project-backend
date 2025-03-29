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
        f"Generate {num_questions} multiple-choice questions (MCQs) from the text below."
        f"Difficulty: {difficulty}. Education Level: {level}."
        "Format each question like this:\n\n"
        "1: What is AI?\n"
        "   a) A fruit\n"
        "   b) A technology\n"
        "   c) A planet\n"
        "   d) A language\n"
        "Answer: b) A technology\n\n"
        "Now generate MCQs from the following text:\n\n"
        f"{text}"
)
    print("Sending request to Gemini API...")  # Debugging
    response = client.models.generate_content(
        model="gemini-2.0-flash-lite", contents=prompt
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

    #print("✅ Parsed MCQs:", mcqs)
    return mcqs