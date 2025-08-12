# frontend/app.py
import os
from pathlib import Path

import streamlit as st
from backend.job_loader import load_jobs
from backend.resume_parser import parse_resume  # assumes you already have this
from backend.prompt_engine import generate_feedback  # uses SIM by default

# ----- Page config
st.set_page_config(page_title="Smart Job Hunter", page_icon="🚀", layout="centered")
st.title("🚀 Smart Job Hunter")
st.caption("Upload your resume and pick (or paste) a job posting to get AI feedback.")

# ----- Wire up secrets → env (so OpenAI client can read them)
# If these keys are in Streamlit Secrets, forward them into env vars:
if "OPENAI_API_KEY" in st.secrets:
    os.environ["OPENAI_API_KEY"] = st.secrets["OPENAI_API_KEY"]
if "USE_SIMULATION" in st.secrets:
    os.environ["USE_SIMULATION"] = str(st.secrets["USE_SIMULATION"])

# Show current mode
use_sim = os.getenv("USE_SIMULATION", "true").lower() == "true"
st.info(f"Mode: **{'SIMULATION' if use_sim else 'LIVE (OpenAI)'}**", icon="⚙️")

# ----- Load jobs (robust: works without data/jobs present)
PROJECT_ROOT = Path(__file__).resolve().parents[1]
JOBS_DIR = PROJECT_ROOT / "data" / "jobs"

@st.cache_data(show_spinner=False)
def _load_jobs_cached(path: Path):
    return load_jobs(path)

jobs = _load_jobs_cached(JOBS_DIR)
job_names = sorted(jobs.keys())

# Always include a "Paste job text..." option
PASTE_OPTION = "➕ Paste a job posting..."
job_options = [PASTE_OPTION] + job_names
selected_job = st.selectbox("Select a job posting:", job_options, index=0)

# If user wants to paste a job
manual_job_text = ""
if selected_job == PASTE_OPTION:
    manual_job_text = st.text_area("Paste the job posting here:", height=200)

# ----- Resume upload
uploaded = st.file_uploader("Upload your resume (PDF / DOCX / TXT)", type=["pdf", "docx", "txt"])
resume_text = ""

if uploaded:
    try:
        resume_text = parse_resume(uploaded)
        st.success("Resume parsed successfully.")
        with st.expander("Preview parsed resume text"):
            st.text_area("", resume_text, height=200)
    except Exception as e:
        st.error(f"Couldn't parse your resume: {e}")

# ----- Action
# Define job_text safely in all paths so we never hit NameError
job_text = manual_job_text if selected_job == PASTE_OPTION else jobs.get(selected_job, "")

col1, col2 = st.columns([1, 2])
with col1:
    run = st.button("Get Feedback", type="primary")

if run:
    # Validate inputs before calling backend
    if not resume_text.strip():
        st.error("Please upload a resume first.")
    elif not job_text.strip():
        st.error("Please select a job or paste a job posting.")
    else:
        with st.spinner("Analyzing…"):
            feedback = generate_feedback(resume_text, job_text)

        st.subheader("🧠 AI Feedback")
        st.text_area("", feedback, height=300)

# Optional dev helpers (enable by adding ALLOW_DEV_TOOLS='true' in secrets)
if st.secrets.get("ALLOW_DEV_TOOLS", "false").lower() == "true":
    st.sidebar.header("Dev tools")
    if st.sidebar.button("🔁 Clear cache & rerun"):
        st.cache_data.clear()
        st.cache_resource.clear()
        st.experimental_rerun()
