from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from app.services.loader import extract_text_from_pdf, extract_text_from_image, extract_text_from_txt
from app.services.vector_store import build_vector_store
from app.services.qa_engine import create_qa_chain, generate_theme_summary

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

@app.post("/upload")
def upload(files: list[UploadFile] = File(...)):
    texts, sources = [], []
    for file in files:
        filename = file.filename
        if file.content_type == "application/pdf":
            extracted = extract_text_from_pdf(file.file, filename)
        elif file.content_type.startswith("image/"):
            extracted = extract_text_from_image(file.file, filename)
        elif file.content_type == "text/plain":
            extracted = extract_text_from_txt(file.file, filename)
        else:
            continue
        for text, source in extracted:
            texts.append(text)
            sources.append(source)
    vs = build_vector_store(texts, sources)
    qa = create_qa_chain(vs)
    return {"message": "Documents processed", "sources": sources}