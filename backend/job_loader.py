# backend/job_loader.py
import os
from pathlib import Path

def load_jobs(folder: str) -> dict:
    p = Path(folder)
    if not p.exists():
        return {}
    jobs = {}
    for txt in p.glob("*.txt"):
        try:
            jobs[txt.name] = txt.read_text(encoding="utf-8")
        except Exception:
            pass
    return jobs
