import os

def load_jobs(folder: str) -> dict:
    jobs = {}
    for fn in os.listdir(folder):
        if fn.endswith(".txt"):
            with open(os.path.join(folder, fn), "r") as f:
                jobs[fn] = f.read()
    return jobs
