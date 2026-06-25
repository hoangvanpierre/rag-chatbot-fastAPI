from fastapi import FastAPI, UploadFile, File, HTTPException
from pydantic import BaseModel
import shutil
import os
from pdf_processor import extract_text_from_pdf, chunk_text
from vector_store import add_chunks_to_db
from rag_chatbot import ask_question, compare_models

app = FastAPI(title = "RAG Chatbot API")

class QuestionRequest(BaseModel):
    question: str
    document_name: str | None = None  # Optional - nếu không truyền, tìm trong tất cả document

class AnswerResponse(BaseModel):
    answer: str

class CompareModelsResponse(BaseModel):
    question: str
    results: list[dict]

@app.post("/upload-pdf")
async def upload_pdf(file: UploadFile = File(...)):
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Chỉ nhận file PDF")
    
    temp_path = f"data/{file.filename}"
    os.makedirs("data", exist_ok=True)
    
    with open(temp_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    text = extract_text_from_pdf(temp_path)
    chunks = chunk_text(text)
    add_chunks_to_db(chunks, document_name=file.filename)
    
    return {
        "message": f"Đã xử lý {file.filename}, tạo {len(chunks)} chunks",
        "document_name": file.filename   # Thêm dòng này để bạn copy chính xác
    }

@app.post("/ask", response_model=AnswerResponse)
async def ask(request: QuestionRequest):
    answer = ask_question(request.question, document_name=request.document_name)
    return AnswerResponse(answer=answer)

@app.post("/compare-models", response_model=CompareModelsResponse)
async def compare(request: QuestionRequest):
    """So sánh câu trả lời + thời gian phản hồi giữa nhiều model Gemini"""
    
    results = compare_models(request.question, document_name=request.document_name)
    
    return CompareModelsResponse(
        question=request.question,
        results=results
    )

@app.get("/")
async def root():
    return {"message": "Rag chatbot API đang hoạt động"}