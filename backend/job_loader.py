import os

FALLBACK_JOB_TEXT = """Customer Success Manager at SaaSCo
Responsibilities: onboarding, CRM (HubSpot/Salesforce), churn reduction, stakeholder management.
"""

def load_jobs(folder: str) -> dict:
    jobs = {}
    if not os.path.isdir(folder):
        # Return a default job so the app always runs on Streamlit
        jobs["job_customer_success_manager.txt"] = FALLBACK_JOB_TEXT
        return jobs

    for fn in os.listdir(folder):
        if fn.endswith(".txt"):
            with open(os.path.join(folder, fn), "r") as f:
                jobs[fn] = f.read()
    if not jobs:
        jobs["job_customer_success_manager.txt"] = FALLBACK_JOB_TEXT
    return jobs
