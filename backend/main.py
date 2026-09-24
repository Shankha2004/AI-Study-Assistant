from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel
import shutil
import os
import uuid

from backend.create_database import create_database
from backend.rag import ask_question, summarize_pdf, generate_quiz

app = FastAPI()

class QuestionRequest(BaseModel):
    question: str
    document_id: str


@app.get("/")
def home():
    return {"message": "AI Study Assistant is running!"}

@app.post("/ask")
def ask(request: QuestionRequest):
    result = ask_question(request.question, request.document_id)

    return{
        "question":request.question,
        "answer":result["answer"],
        "sources":result["sources"]
    }

@app.post("/upload")
def upload_pdf(file: UploadFile = File(...)):

    os.makedirs("uploads", exist_ok=True)

    document_id = str(uuid.uuid4())

    file_path = os.path.join(
        "uploads",
        f"{document_id}_{file.filename}"
    )

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    chunks_indexed=create_database(file_path, document_id)

    return {
        "message": "PDF uploaded and processed successfully",
        "document_id": document_id,
        "filename": file.filename,
        "chunks_indexed": chunks_indexed
    }

@app.post("/summarize")
def summarize(document_id: str):

    summary = summarize_pdf(document_id)

    return {
        "summary": summary
    }

@app.post("/quiz")
def quiz(document_id: str):

    quiz = generate_quiz(document_id)

    return {
        "quiz": quiz
    }