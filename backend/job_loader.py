# backend/job_loader.py
from pathlib import Path
from typing import Dict

def load_jobs(folder: str | Path) -> Dict[str, str]:
    """
    Load *.txt job postings from a folder.
    If the folder is missing or empty, return a built-in sample job.
    """
    p = Path(folder)
    jobs: Dict[str, str] = {}

    if p.exists() and p.is_dir():
        for fn in sorted(p.glob("*.txt")):
            try:
                jobs[fn.name] = fn.read_text(encoding="utf-8", errors="ignore")
            except Exception:
                # Skip files we can't read cleanly
                continue

    if not jobs:
        jobs["sample_job.txt"] = (
            "Title: Junior AI/ML Engineer\n"
            "Company: ExampleCo\n"
            "Responsibilities:\n"
            "- Build small NLP utilities in Python\n"
            "- Clean and process text data\n"
            "- Write Streamlit prototypes\n"
            "Requirements:\n"
            "- Python, pandas, scikit-learn basics\n"
            "- Prompt engineering familiarity\n"
            "- Clear communication\n"
            "Nice to have:\n"
            "- FastAPI, embeddings, vector search\n"
        )

    return jobs
