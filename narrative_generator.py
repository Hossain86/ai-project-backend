import re
import os
from google import genai
from dotenv import load_dotenv
load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=API_KEY)

def generateOpenEnded(text, num_questions, level, difficulty):
    """Generate 10 numbered OpenEnded questions and answers."""
    prompt = (
        f"Generate {num_questions} narrative questions and answer from the text below. Difficulty: {difficulty}. Education Level: {level} with detailed answers (50-150 words). "
        "Keep the text's explanation style and include examples if possible.\n\n"
        "Format:\n"
        "1. What is AI?\n"
        "✅ Answer: AI (Artificial Intelligence) simulates human intelligence in machines, enabling tasks like speech recognition and decision-making. "
        "Examples: Siri, Alexa, self-driving cars.\n\n"
        f"Text:\n{text}"
    )
    print("Sending request to Gemini API...")  # Debugging
    print(f"Prompt: {prompt[:500]}")  # Print the first 500 chars
    response = client.models.generate_content(
        model="gemini-2.0-flash-lite", contents=prompt
    )
    print(f"Raw API Response: {response.text}") 
    if not response or not response.text:
        return {"error": "Failed to generate OpenEnded questions."}
    
    # Extract questions and answers with numbers
    pattern = re.compile(r'(\d+)\.\s*(.*?)\n\s*✅ Answer:\s*(.*?)(?:\n|$)', re.DOTALL)
    qa_pairs = pattern.findall(response.text)
    print(f"Expected QA pairs: {qa_pairs}")  # Debugging
    return [
        {"number": int(num), "question": q.strip(), "answer": a.strip()}
        for num, q, a in qa_pairs
    ]
