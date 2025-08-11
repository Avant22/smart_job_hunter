# frontend/app.py

import sys, os
from pathlib import Path

# Make project root importable (keep this if you already added it)
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir)))

import streamlit as st
from backend.resume_parser import parse_resume
from backend.job_loader import load_jobs
from backend.matcher import find_best_match
from backend.prompt_engine import generate_feedback

# 🔧 Resolve paths from project root no matter where Streamlit runs
BASE_DIR = Path(__file__).resolve().parents[1]
JOBS_DIR = BASE_DIR / "data" / "jobs"
RESUMES_DIR = BASE_DIR / "data" / "resumes"
RESUMES_DIR.mkdir(parents=True, exist_ok=True)  # ensure upload dir exists

st.set_page_config(page_title="Smart Job Hunter", layout="centered")
st.title("🚀 Smart Job Hunter")
st.markdown("Upload your resume and select (or auto-detect) a job posting to get AI-powered feedback.")

# Load jobs using absolute path
jobs = load_jobs(str(JOBS_DIR))
job_names = list(jobs.keys())
if not job_names:
    st.warning("No job files found in `data/jobs`. Add one or more `.txt` job postings to the repo.")

uploaded = st.file_uploader("Upload Resume (PDF or DOCX)", type=["pdf", "docx"])
selected_job = st.selectbox("Or choose a job posting", ["<Auto-detect>"] + job_names)

if uploaded:
    save_path = RESUMES_DIR / uploaded.name
    with open(save_path, "wb") as f:
        f.write(uploaded.getbuffer())
    resume_text = parse_resume(str(save_path))

    if selected_job == "<Auto-detect>" and jobs:
        best_job, score = find_best_match(resume_text, jobs)
        st.write(f"🔍 **Best match:** {best_job} (score: {score:.2f})")
        job_to_use = best_job
    else:
        job_to_use = selected_job if selected_job in jobs else None

    if job_to_use and st.button("Get Feedback"):
        job_text = jobs[job_to_use]
        feedback = generate_feedback(resume_text, job_text)
        st.subheader("🧠 AI Feedback")
        st.text_area("", feedback, height=300)