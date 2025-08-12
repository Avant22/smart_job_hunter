# frontend/app.py
import os
import sys
from pathlib import Path

# --- Ensure project root is on sys.path so `backend.*` imports work ---
PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import streamlit as st  # noqa: E402

from backend.job_loader import load_jobs  # noqa: E402
from backend.resume_parser import parse_resume  # noqa: E402
from backend.prompt_engine import generate_feedback  # noqa: E402

# ----- Page config
st.set_page_config(page_title="Smart Job Hunter", page_icon="🚀", layout="centered")
st.title("🚀 Smart Job Hunter")
st.caption("Upload your resume and pick (or paste) a job posting to get AI feedback.")

# ----- Mirror secrets to env so backend can read them
if "OPENAI_API_KEY" in st.secrets:
    os.environ["OPENAI_API_KEY"] = st.secrets["OPENAI_API_KEY"]
if "USE_SIMULATION" in st.secrets:
    os.environ["USE_SIMULATION"] = str(st.secrets["USE_SIMULATION"])

use_sim = os.getenv("USE_SIMULATION", "true").lower() == "true"
st.info(f"Mode: **{'SIMULATION' if use_sim else 'LIVE (OpenAI)'}**", icon="⚙️")

# ----- Load jobs (with safe fallback to sample)
JOBS_DIR = PROJECT_ROOT / "data" / "jobs"

@st.cache_data(show_spinner=False)
def _load_jobs_cached(path: Path):
    return load_jobs(path)

jobs = _load_jobs_cached(JOBS_DIR)
job_names = sorted(jobs.keys())

PASTE_OPTION = "➕ Paste a job posting..."
job_choice = st.selectbox("Select a job posting:", [PASTE_OPTION] + job_names, index=0)

manual_job_text = ""
if job_choice == PASTE_OPTION:
    manual_job_text = st.text_area("Paste the job posting here:", height=200)

# ----- Resume upload
uploaded = st.file_uploader("Upload your resume (PDF / DOCX / TXT)", type=["pdf", "docx", "txt"])

resume_text = ""
if uploaded:
    try:
        resume_text = parse_resume(uploaded)
        st.success("Resume parsed successfully.")
        with st.expander("Preview parsed resume text"):
            st.text_area("", resume_text, height=220)
    except Exception as e:
        st.error(f"Couldn't parse your resume: {e}")

# Define job_text in all cases to avoid NameError
job_text = manual_job_text if job_choice == PASTE_OPTION else jobs.get(job_choice, "")

# ----- Run analysis
run = st.button("Get Feedback", type="primary")

if run:
    if not resume_text.strip():
        st.error("Please upload a resume first.")
    elif not job_text.strip():
        st.error("Please select a job or paste a job posting.")
    else:
        with st.spinner("Analyzing…"):
            feedback = generate_feedback(resume_text, job_text)
        st.subheader("🧠 AI Feedback")
        st.text_area("", feedback, height=320)

# Optional dev helper
if str(st.secrets.get("ALLOW_DEV_TOOLS", "false")).lower() == "true":
    st.sidebar.header("Dev tools")
    if st.sidebar.button("🔁 Clear cache & rerun"):
        st.cache_data.clear()
        st.cache_resource.clear()
        st.experimental_rerun()
