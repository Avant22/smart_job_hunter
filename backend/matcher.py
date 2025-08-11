import os, re
from dotenv import load_dotenv

load_dotenv()
USE_SIM = os.getenv("USE_SIMULATION", "false").lower() == "true"

# --- simple token overlap for SIM mode ---
def _tokens(s: str) -> set[str]:
    return set(re.findall(r"\b[a-z]{3,}\b", s.lower()))

def _jaccard(a: str, b: str) -> float:
    A, B = _tokens(a), _tokens(b)
    return len(A & B) / max(1, len(A | B))

def find_best_match(resume: str, jobs: dict) -> tuple[str, float]:
    if not jobs:
        return None, 0.0

    if USE_SIM:
        scores = {name: _jaccard(resume, txt) for name, txt in jobs.items()}
        best = max(scores, key=scores.get)
        return best, scores[best]

    # --- LIVE mode: embeddings + cosine similarity ---
    from openai import OpenAI
    from sklearn.metrics.pairwise import cosine_similarity

    client = OpenAI()

    def embed(text: str):
        out = client.embeddings.create(model="text-embedding-3-small", input=text)
        return out.data[0].embedding

    emb_resume = [embed(resume)]
    best_name, best_score = None, -1.0
    for name, txt in jobs.items():
        emb_job = [embed(txt)]
        score = float(cosine_similarity(emb_resume, emb_job)[0][0])
        if score > best_score:
            best_name, best_score = name, score
    return best_name, best_score
