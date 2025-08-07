import os
from dotenv import load_dotenv
load_dotenv()
import openai
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

openai.api_key = os.getenv("OPENAI_API_KEY")

def embed_text(text: str) -> list:
    resp = openai.Embedding.create(input=[text], model="text-embedding-ada-002")
    return resp["data"][0]["embedding"]

def find_best_match(resume: str, jobs: dict) -> tuple:
    emb_resume = embed_text(resume)
    scores = {}
    for name, txt in jobs.items():
        emb_job = embed_text(txt)
        scores[name] = cosine_similarity([emb_resume], [emb_job])[0][0]
    best = max(scores, key=scores.get)
    return best, scores[best]
