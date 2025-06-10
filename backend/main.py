from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv
from app.models import QueryRequest
from app.document_handler import extract_text
from app.vectorstore import create_vectorstore
from app.qa import query_vectorstore

load_dotenv()
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

document_texts = []

@app.post("/upload/")
async def upload(file: UploadFile = File(...)):
    try:
        UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), "uploads")
        os.makedirs(UPLOAD_FOLDER, exist_ok=True)

        file_path = os.path.join(UPLOAD_FOLDER, file.filename)
        print(f"Saving to: {file_path}")

        with open(file_path, "wb") as f:
            f.write(await file.read())

        return {"status": "uploaded", "filename": file.filename}
    except Exception as e:
        return {"error": str(e)}

@app.post("/ingest/")
def ingest():
    if not os.path.exists(UPLOAD_FOLDER):
        return {"error": "No uploads folder found."}

    text_chunks = []
    for filename in os.listdir(UPLOAD_FOLDER):
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        text = extract_text(file_path)
        if text.strip():
            text_chunks.append(text)

    if not text_chunks:
        return {"error": "No text could be extracted from uploaded files."}

    create_vectorstore(text_chunks)
    return {"status": "vectorstore created"}

@app.post("/query/")
def query(req: QueryRequest):
    result = query_vectorstore(req.question)
    return {"answer": result['result']}
