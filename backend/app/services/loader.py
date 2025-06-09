from PyPDF2 import PdfReader
from PIL import Image
from ..config import OCR_ENGINE


if OCR_ENGINE == "paddleocr":
    from paddleocr import PaddleOCR
    ocr_engine = PaddleOCR(use_angle_cls=True, lang='en')
    def run_ocr(img):
        result = ocr_engine.ocr(img, cls=True)
        return "\n".join([line[1][0] for line in result[0]])
else:
    import pytesseract
    def run_ocr(img):
        return pytesseract.image_to_string(img)

def extract_text_from_pdf(file, filename):
    texts = []
    reader = PdfReader(file)
    for i, page in enumerate(reader.pages):
        text = page.extract_text()
        if text:
            texts.append((text, f"{filename} - Page {i+1}"))
    return texts

def extract_text_from_image(file, filename):
    img = Image.open(file)
    text = run_ocr(img)
    return [(text, f"{filename} - Image OCR")]

def extract_text_from_txt(file, filename):
    content = file.read().decode("utf-8")
    return [(content, f"{filename} - Text")]