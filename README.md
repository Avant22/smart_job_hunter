https://huggingface.co/spaces/avant22/smart_job_hunter
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

