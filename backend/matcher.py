# backend/matcher.py
import os, re
from dotenv import load_dotenv

load_dotenv()
USE_SIM = os.getenv("USE_SIMULATION", "true").lower() == "true"

def _tokens(s: str) -> set[str]:
    return set(re.findall(r"\b[a-z]{3,}\b", s.lower()))

def _jaccard(a: str, b: str) -> float:
    A, B = _tokens(a), _tokens(b)
    return len(A & B) / max(1, len(A | B))

def find_best_match(resume: str, jobs: dict) -> tuple[str | None, float]:
    if not jobs:
        return None, 0.0

    if USE_SIM:
        scores = {name: _jaccard(resume, txt) for name, txt in jobs.items()}
        best = max(scores, key=scores.get)
        return best, scores[best]

    # LIVE (optional)
    try:
        from openai import OpenAI
        from sklearn.metrics.pairwise import cosine_similarity

        client = OpenAI()
        def embed(t: str):
            v = client.embeddings.create(model="text-embedding-3-small", input=t)
            return v.data[0].embedding

        r = [embed(resume)]
        best, best_score = None, -1.0
        for name, txt in jobs.items():
            score = float(cosine_similarity(r, [embed(txt)])[0][0])
            if score > best_score:
                best, best_score = name, score
        return best, best_score
    except Exception:
        scores = {name: _jaccard(resume, txt) for name, txt in jobs.items()}
        best = max(scores, key=scores.get)
        return best, scores[best]
