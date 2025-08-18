# Smart Job Hunter 🚀

**Smart Job Hunter** is a full-stack AI-powered career assistant.  
It parses resumes, matches them against job postings using embeddings, and generates GPT-4 style feedback to help candidates improve their applications.  

- 📝 Upload a resume (TXT, DOCX, PDF supported locally)  
- 📊 Match against one or more job postings  
- 🤖 Get AI-generated feedback and suggestions  
- 🎭 Includes **simulation mode** (no API key required) for portfolio/demo purposes  

---

## Live Demo 🌍
Try it here: [Smart Job Hunter on Hugging Face](https://huggingface.co/spaces/avant22/smart_job_hunter)

---

## Features
- **Resume Parsing**: Extracts text from resumes (TXT, DOCX, PDF).  
- **Job Loader**: Auto-detects job postings from `data/jobs/`.  
- **Matching Engine**: Embedding-based similarity scoring (planned).  
- **AI Feedback**: Simulated GPT-style coaching to improve resumes.  
- **Streamlit Frontend**: Interactive UI for uploads & feedback.  
- **FastAPI Backend**: Modular structure ready for real-world scaling.  

---

## Tech Stack
- **Python 3.11+**  
- [Streamlit](https://streamlit.io/) (frontend)  
- [FastAPI](https://fastapi.tiangolo.com/) (API backend)  
- [Hugging Face Spaces](https://huggingface.co/spaces) (cloud deployment)  
- [OpenAI API](https://platform.openai.com/) (optional, live mode)  
- [python-docx](https://python-docx.readthedocs.io/), [PyPDF2](https://pypi.org/project/PyPDF2/) (resume parsing)  

---

## Local Setup

```bash
git clone https://github.com/Avant22/smart_job_hunter.git
cd smart_job_hunter
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
streamlit run frontend/app.py
Project Structure
bash
Copy
Edit
smart_job_hunter/
├── api/                 # FastAPI backend
├── backend/             # Resume parsing, job matching, prompt engine
├── frontend/            # Streamlit app
├── data/jobs/           # Example job postings
├── requirements.txt     # Dependencies
├── runtime.txt          # Python version for deployment
└── README.md
Portfolio Notes
This project is designed for simulation mode (no API keys required).

In real-world use, you can enable the OpenAI API for live resume feedback.

Built as a portfolio showcase for AI integration & prompt engineering.

yaml
Copy
Edit

---

## 3. Polished README.md for Hugging Face Space

Your Hugging Face `README.md` should be simpler (focus on demo & usage):

```markdown
# Smart Job Hunter 🚀

AI-powered resume assistant.  

📂 Upload your resume and match it against job postings.  
🤖 Get instant AI-style feedback on how to improve your application.  
🎭 **Simulation Mode** → runs without paid APIs (safe for demos).  

---

## How to Use
1. Upload a resume file (`.txt` supported here).  
2. Select a job posting (or let the app auto-detect).  
3. Click **Get Feedback**.  

You’ll receive simulated AI suggestions such as:  
- Add missing keywords from the job.  
- Quantify achievements with numbers.  
- Mirror job phrasing & highlight relevant tools.  

---

## About
This app is part of a **portfolio project** showing:  
- End-to-end AI integration (Streamlit + FastAPI)  
- Resume parsing and job posting ingestion  
- AI prompt engineering (simulation & live-ready)  

---

## Links
- 🔗 [Source Code on GitHub](https://github.com/Avant22/smart_job_hunter)  
- 🌍 [Live Hugging Face Demo](https://huggingface.co/spaces/avant22/smart_job_hunter)  
