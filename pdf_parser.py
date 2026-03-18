import fitz  # PyMuPDF
import os
import shutil

UPLOAD_FOLDER = "uploads"

def save_pdf(uploaded_file) -> str:
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    file_path = os.path.join(UPLOAD_FOLDER, uploaded_file.name)
    with open(file_path, "wb") as f:
        shutil.copyfileobj(uploaded_file, f)
    return file_path

def extract_text_from_pdf(uploaded_file) -> str:
    file_path = save_pdf(uploaded_file)

    text = ""
    with fitz.open(file_path) as pdf:
        for page in pdf:
            text += page.get_text() + "\n"
    return text.strip()
