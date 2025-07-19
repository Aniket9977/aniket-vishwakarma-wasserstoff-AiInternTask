# main.py
import os
from pathlib import Path
from datetime import datetime
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn

# Initialize FastAPI
app = FastAPI(title="Document Research API")

# Simple CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configuration
UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

# Simple data model
class QueryRequest(BaseModel):
    question: str

# Global variables
uploaded_files = []
vectorstore_ready = False

# Health check
@app.get("/")
@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "message": "Document Research API is running",
        "timestamp": datetime.now().isoformat()
    }

# Upload endpoint
@app.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    try:
        if not file.filename:
            raise HTTPException(status_code=400, detail="No file provided")
        
        # Save file
        file_path = UPLOAD_DIR / file.filename
        with open(file_path, "wb") as buffer:
            content = await file.read()
            buffer.write(content)
        
        # Track uploaded file
        uploaded_files.append({
            "filename": file.filename,
            "path": str(file_path),
            "timestamp": datetime.now().isoformat()
        })
        
        return {
            "message": f"File {file.filename} uploaded successfully",
            "total_files": len(uploaded_files)
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")

# Ingest endpoint
@app.post("/ingest/")
async def ingest_documents():
    global vectorstore_ready
    
    try:
        if not uploaded_files:
            raise HTTPException(status_code=400, detail="No files uploaded")
        
        # Simulate processing
        vectorstore_ready = True
        
        return {
            "message": "Documents processed successfully",
            "processed_files": len(uploaded_files)
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Processing failed: {str(e)}")

# Query endpoint
@app.post("/query/")
async def query_documents(request: QueryRequest):
    try:
        if not vectorstore_ready:
            raise HTTPException(status_code=400, detail="Documents not processed yet")
        
        if not request.question.strip():
            raise HTTPException(status_code=400, detail="Question cannot be empty")
        
        # Simple response
        answer = f"Based on {len(uploaded_files)} uploaded documents, here's an answer to your question: '{request.question}'\n\nThis is a placeholder response. In production, this would use AI to analyze your documents and provide intelligent answers."
        
        return {
            "answer": answer,
            "sources": [f["filename"] for f in uploaded_files[:3]]
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Query failed: {str(e)}")

# Status endpoint
@app.get("/status/")
async def get_status():
    return {
        "uploaded_files": len(uploaded_files),
        "vectorstore_ready": vectorstore_ready
    }

# Clear data endpoint
@app.delete("/clear/")
async def clear_data():
    global vectorstore_ready, uploaded_files
    
    try:
        # Clear files
        for file_info in uploaded_files:
            file_path = Path(file_info["path"])
            if file_path.exists():
                file_path.unlink()
        
        # Reset
        uploaded_files = []
        vectorstore_ready = False
        
        return {"message": "All data cleared"}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Clear failed: {str(e)}")

# Run the app
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)