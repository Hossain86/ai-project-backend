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
        f"Generate {num_questions} narrative questions and answer from the text below with  answers (50-150 words). "
        "Keep the text's explanation style and include examples if possible.\n\n"
        "Format:\n"
        "1. What is AI?\n"
        "✅ Answer: Artificial intelligence (AI) refers to the ability of computers to perform tasks that typically require human intelligence. This includes activities like learning, problem-solving, and decision-making. AI systems are often designed using algorithms, which are sets of instructions that enable computers to analyze data and identify patterns. There are different types of AI, ranging from narrow AI, which is designed for a specific task like playing chess, to general AI, which could potentially perform any intellectual task a human can. AI is rapidly evolving, impacting various sectors such as healthcare, finance, and transportation, and raising important questions about its ethical implications and future impact on society. "
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
