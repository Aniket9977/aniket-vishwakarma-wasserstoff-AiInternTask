import pdfplumber
import pytesseract
from PIL import Image
import os

def extract_text(file_path):
    ext = file_path.split('.')[-1].lower()
    if ext == "pdf":
        with pdfplumber.open(file_path) as pdf:
            return "\n".join([page.extract_text() or "" for page in pdf.pages])
    elif ext in ["jpg", "jpeg", "png"]:
        return pytesseract.image_to_string(Image.open(file_path))
    return ""
