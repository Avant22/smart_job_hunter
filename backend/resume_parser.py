# backend/resume_parser.py
from io import BytesIO

import PyPDF2
from docx import Document

def parse_resume(uploaded_file) -> str:
    """
    Accepts a Streamlit UploadedFile and returns extracted text.
    Supports PDF, DOCX, and TXT.
    """
    name = (uploaded_file.name or "").lower()
    data = uploaded_file.read()  # bytes

    if name.endswith(".pdf"):
        try:
            reader = PyPDF2.PdfReader(BytesIO(data))
            texts = [(p.extract_text() or "") for p in reader.pages]
            return "\n".join(texts).strip()
        except Exception as e:
            raise RuntimeError(f"PDF parse failed: {e}")

    if name.endswith(".docx"):
        try:
            doc = Document(BytesIO(data))
            return "\n".join(p.text for p in doc.paragraphs).strip()
        except Exception as e:
            raise RuntimeError(f"DOCX parse failed: {e}")

    if name.endswith(".txt"):
        try:
            return data.decode("utf-8", errors="ignore")
        except Exception as e:
            raise RuntimeError(f"TXT parse failed: {e}")

    # Fallback: try decoding anyway
    try:
        return data.decode("utf-8", errors="ignore")
    except Exception:
        raise RuntimeError("Unsupported file type. Please upload PDF, DOCX, or TXT.")
