# backend/prompt_engine.py
import os
from dotenv import load_dotenv

# Load .env for local dev; on Streamlit Cloud we use st.secrets (forwarded by the app)
load_dotenv()

USE_SIM = os.getenv("USE_SIMULATION", "true").lower() == "true"

PROMPT_TEMPLATE = """
You are an expert AI Software Developer coach.
Here is the job posting:
{job_text}

Here is the candidate’s resume:
{resume_text}

Please provide:
1) A match score explanation.
2) Three bullet-pointed suggestions to improve the resume.
"""

def generate_feedback(resume_text: str, job_text: str) -> str:
    """
    Returns simulated feedback if USE_SIM==true.
    Otherwise calls OpenAI Chat Completions (>=1.0 API) safely.
    """
    if USE_SIM:
        return (
            "Simulated feedback:\n"
            "- Add missing keywords from the job (SaaS, CRM/HubSpot, onboarding).\n"
            "- Quantify achievements (users/%/time saved).\n"
            "- Align bullets with responsibilities; mirror job phrasing and tools."
        )

    # LIVE mode
    try:
        # Import inside the live branch so SIM mode never imports openai
        from openai import OpenAI
        client = OpenAI()  # Reads OPENAI_API_KEY from env (set by Streamlit app)

        prompt = PROMPT_TEMPLATE.format(job_text=job_text, resume_text=resume_text)
        resp = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
        )
        return resp.choices[0].message.content or "(No content returned)"
    except Exception as e:
        # Graceful fallback to simulated advice
        return (
            f"(Simulation fallback due to API error: {e})\n"
            "- Add missing keywords from the job (SaaS, CRM/HubSpot, onboarding).\n"
            "- Quantify achievements (users/%/time saved).\n"
            "- Align bullets with responsibilities; mirror job phrasing and tools."
        )
