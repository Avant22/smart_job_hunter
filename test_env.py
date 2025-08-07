# test_env.py
from dotenv import load_dotenv
import os

load_dotenv()   # loads variables from .env
print("OPENAI_API_KEY is:", os.getenv("OPENAI_API_KEY"))
