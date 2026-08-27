import os
import json

from openai import OpenAI
from dotenv import load_dotenv

from models.candidate import CandidateProfile


# Load .env
load_dotenv()


# OpenRouter client
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY")
)


# Primary model
MODEL_NAME = "minimax/minimax-m2.7:free"


def extract_candidate_profile(resume_text):

    prompt = f"""
You are an expert resume information extraction system.

Analyze the resume below and extract structured candidate information.

Return ONLY valid JSON.

Use exactly this structure:

{{
    "name": "",
    "email": "",
    "phone": "",
    "skills": [],
    "education": [],
    "experience": [],
    "projects": [],
    "certifications": [],
    "career_interests": []
}}

Rules:

1. Extract information only from the resume.
2. Do not invent information.
3. If information is missing, use an empty string or empty list.
4. Skills must be a list of strings.

5. Education must contain:
   degree, institution, year

6. Experience must contain:
   company, role, duration, description

7. Projects must contain:
   name, description, technologies

8. IMPORTANT:
   technologies MUST always be a JSON list of strings.

   Correct:
   "technologies": ["Python", "Deep Learning"]

   Incorrect:
   "technologies": "Python, Deep Learning"

9. Certifications must be a list of strings.

10. Career interests must be a list of strings.

Resume:

{resume_text}
"""

    response = client.chat.completions.create(

        # Primary model
        model=MODEL_NAME,

        messages=[
            {
                "role": "system",
                "content": "You extract structured information from resumes."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],

        temperature=0,

        # OpenRouter model fallback
        extra_body={
            "models": [
                "minimax/minimax-m2.7:free",
                "openai/gpt-4o-mini",
                "google/gemini-2.5-flash"
            ]
        }
    )

    content = response.choices[0].message.content

    # Remove markdown code fences
    content = content.replace("```json", "")
    content = content.replace("```", "")
    content = content.strip()

    # Convert JSON to Python dictionary
    data = json.loads(content)

    # Convert dictionary to CandidateProfile
    profile = CandidateProfile(**data)

    return profile