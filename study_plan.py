import os
from google import genai
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=API_KEY)

def generate_study_plan(name, age, education_level, days_left, subjects, preferences, availability):
    prompt = f"""
        Generate a highly personalized study plan for {name}, a {age}-year-old {education_level} student.
        They have {days_left} days left to prepare for the exam.
        They need to focus on the following subjects: {', '.join(subjects)}.
        Their study preferences include: {preferences}.
        They are available for studying during: {availability}.
        
        Create a structured day-wise plan that ensures balanced coverage of all subjects,
        considers revision time, and optimizes learning based on preferences.
        
        The plan should be clear, practical, short and effective.
    """
    
    response = client.models.generate_content(
        model="gemini-2.0-flash-lite", contents=prompt
    )

    if not response or not response.text:
        return {"error": "Failed to generate study plan"}

    return response.text
