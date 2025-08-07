import os
from dotenv import load_dotenv
load_dotenv()
import openai

openai.api_key = os.getenv("OPENAI_API_KEY")

PROMPT_TEMPLATE = """
You are an expert AI Software Developer coach.
Here is the job posting:
{job_text}

Here is the candidate’s resume:
{resume_text}

Please provide:
1. A match score explanation.
2. Three bullet-pointed suggestions to improve the resume.
"""

def generate_feedback(resume_text: str, job_text: str) -> str:
    prompt = PROMPT_TEMPLATE.format(job_text=job_text, resume_text=resume_text)
    resp = openai.ChatCompletion.create(
        model="gpt-4-turbo",
        messages=[{"role": "user", "content": prompt}]
    )
    return resp.choices[0].message.content
