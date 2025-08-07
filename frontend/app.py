# frontend/app.py
import sys, os
# Add project root to Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir)))

import streamlit as st
from backend.resume_parser import parse_resume
from backend.job_loader      import load_jobs
from backend.matcher         import find_best_match
from backend.prompt_engine   import generate_feedback
import os

# Page layout
st.set_page_config(page_title="Smart Job Hunter", layout="centered")
st.title("🚀 Smart Job Hunter")
st.markdown("Upload your resume and select (or auto-detect) a job posting to get AI-powered feedback.")

# Load available jobs
jobs = load_jobs("data/jobs")
job_names = list(jobs.keys())

# File uploader
uploaded = st.file_uploader("Upload Resume (PDF or DOCX)", type=["pdf", "docx"])
selected_job = st.selectbox("Or choose a job posting", ["<Auto-detect>"] + job_names)

if uploaded:
    # Save upload to data/resumes/
    save_path = os.path.join("data", "resumes", uploaded.name)
    with open(save_path, "wb") as f:
        f.write(uploaded.getbuffer())
    resume_text = parse_resume(save_path)

    # Find best match if auto-detect
    if selected_job == "<Auto-detect>":
        best_job, score = find_best_match(resume_text, jobs)
        st.write(f"🔍 **Best match:** {best_job} (score: {score:.2f})")
        job_to_use = best_job
    else:
        job_to_use = selected_job

    # Show the “Get Feedback” button
    if st.button("Get Feedback"):
        job_text = jobs[job_to_use]
        feedback = generate_feedback(resume_text, job_text)
        st.subheader("🧠 AI Feedback")
        st.text_area("", feedback, height=300)
