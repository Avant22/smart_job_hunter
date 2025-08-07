from fastapi import FastAPI, UploadFile, File
from backend.resume_parser import parse_resume
from backend.job_loader import load_jobs
from backend.matcher import find_best_match
from backend.prompt_engine import generate_feedback

app = FastAPI()
jobs = load_jobs("data/jobs")

@app.post("/analyze/")
async def analyze(resume_file: UploadFile = File(...), job_filename: str = None):
    # parse resume
    content = await resume_file.read()
    path = f"data/resumes/{resume_file.filename}"
    with open(path, "wb") as f:
        f.write(content)
    resume_text = parse_resume(path)
    # pick a job
    if job_filename is None:
        job_filename, score = find_best_match(resume_text, jobs)
    job_text = jobs[job_filename]
    feedback = generate_feedback(resume_text, job_text)
    return {"job": job_filename, "feedback": feedback}
