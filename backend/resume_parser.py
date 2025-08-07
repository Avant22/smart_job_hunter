import os, PyPDF2, docx

def parse_resume(path: str) -> str:
    ext = os.path.splitext(path)[1].lower()
    text = ""
    if ext == ".pdf":
        reader = PyPDF2.PdfReader(path)
        for p in reader.pages:
            text += p.extract_text() or ""
    elif ext == ".docx":
        doc = docx.Document(path)
        for para in doc.paragraphs:
            text += para.text + "\n"
    else:
        with open(path, "r") as f:
            text = f.read()
    return text
