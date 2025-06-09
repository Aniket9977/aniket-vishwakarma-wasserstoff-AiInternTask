import os
from dotenv import load_dotenv

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OCR_ENGINE = os.getenv("OCR_ENGINE", "pytesseract")