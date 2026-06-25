# RAG Chatbot with FastAPI

A Retrieval-Augmented Generation (RAG) chatbot that answers questions based on the content of uploaded PDF documents. Built as a portfolio project to demonstrate core AI Engineering skills: LLM API integration, vector search, and backend API development.

🇻🇳 [Đọc bằng Tiếng Việt](#rag-chatbot-với-fastapi)

## Features

- **PDF Upload & Processing** — extracts and chunks text from any PDF document
- **Vector Search** — stores document chunks as embeddings in ChromaDB for semantic search
- **Multi-Document Support** — supports multiple PDFs simultaneously, with metadata filtering to query a specific document
- **LLM-Powered Answers** — uses Google Gemini API to generate answers grounded in retrieved context
- **Hallucination Control** — explicitly instructs the model to say "not found" when the answer isn't in the source document, rather than guessing
- **Graceful Error Handling** — catches upstream API failures (e.g. model overload) and returns a clean message instead of crashing
- **Dockerized** — fully containerized for consistent deployment across environments

## Architecture

```
PDF Upload
    │
    ▼
Text Extraction (pypdf)
    │
    ▼
Chunking (sliding window with overlap)
    │
    ▼
Embedding + Storage (ChromaDB, with document_name metadata)
    │
    ▼
User Question ──► Embed Query ──► Similarity Search (filtered by document_name)
                                          │
                                          ▼
                              Retrieved Chunks + Question
                                          │
                                          ▼
                                 Gemini API (generation)
                                          │
                                          ▼
                                       Answer
```

All of the above is exposed via a FastAPI REST API and packaged into a Docker container.

## Tech Stack

| Component | Technology |
|---|---|
| Language | Python |
| LLM | Google Gemini API (`gemini-2.5-flash`) via `google-genai` SDK |
| Vector Database | ChromaDB (local, persistent) |
| PDF Parsing | pypdf |
| API Framework | FastAPI |
| Containerization | Docker |

## API Endpoints

### `POST /upload-pdf`
Uploads a PDF, extracts text, chunks it, and stores it in the vector database.

```bash
curl -X 'POST' 'http://127.0.0.1:8000/upload-pdf' \
  -H 'Content-Type: multipart/form-data' \
  -F 'file=@your_document.pdf;type=application/pdf'
```

**Response:**
```json
{
  "message": "Đã xử lý your_document.pdf, tạo 58 chunks",
  "document_name": "your_document.pdf"
}
```

### `POST /ask`
Asks a question. Optionally scoped to a specific document via `document_name`.

```bash
curl -X 'POST' 'http://127.0.0.1:8000/ask' \
  -H 'Content-Type: application/json' \
  -d '{
    "question": "What is the role of mathematics in AI?",
    "document_name": "your_document.pdf"
  }'
```

**Response:**
```json
{
  "answer": "Mathematics provides the tools to understand and improve AI systems..."
}
```

## Getting Started

### Prerequisites
- Docker Desktop installed and running
- A free Gemini API key from [Google AI Studio](https://aistudio.google.com/apikey)

### Setup

1. Clone this repository
```bash
git clone https://github.com/hoangvanpierre/rag-chatbot-fastAPI.git
cd rag-chatbot-fastAPI
```

2. Create a `.env` file in the root directory
```
GEMINI_API_KEY=your_key_here
```

3. Build the Docker image
```bash
docker build -t rag-chatbot .
```

4. Run the container
```bash
docker run -p 8000:8000 --env-file .env rag-chatbot
```

5. Open the interactive API docs
```
http://127.0.0.1:8000/docs
```

### Running locally without Docker (for development)

```bash
python -m venv venv
venv\Scripts\activate          # Windows
pip install -r requirements.txt
uvicorn main:app --reload
```

## Key Engineering Decisions

- **Chunking with overlap**: text is split into overlapping chunks so that information sitting at a chunk boundary isn't lost during retrieval.
- **Metadata filtering**: each chunk is tagged with its source `document_name` at ingestion time. This prevents context from different documents being mixed together during retrieval when multiple PDFs are stored.
- **Explicit grounding instruction**: the prompt explicitly tells the model to admit when an answer isn't found in the provided context, reducing hallucination.
- **Graceful degradation**: upstream LLM API failures (e.g. `503` overload errors) are caught and returned as a clean, user-facing message rather than a raw `500` error.

## Possible Improvements

- Support for additional file types (DOCX, TXT, images via OCR)
- Streaming responses for faster perceived latency
- Conversation history / multi-turn context
- Swap the local embedding model for a hosted embedding API for better multilingual support

---

# RAG Chatbot với FastAPI

Một chatbot RAG (Retrieval-Augmented Generation) trả lời câu hỏi dựa trên nội dung file PDF được upload. Đây là project portfolio nhằm thể hiện các kỹ năng cốt lõi của AI Engineer: tích hợp LLM API, vector search, và phát triển backend API.

🇬🇧 [Read in English](#rag-chatbot-with-fastapi)

## Tính năng

- **Upload & xử lý PDF** — trích xuất và chia nhỏ (chunk) text từ bất kỳ file PDF nào
- **Tìm kiếm theo vector** — lưu các chunk dưới dạng embedding trong ChromaDB để tìm kiếm theo ngữ nghĩa
- **Hỗ trợ nhiều tài liệu** — cho phép lưu nhiều PDF cùng lúc, có metadata filtering để hỏi đúng vào 1 tài liệu cụ thể
- **Trả lời bằng LLM** — dùng Google Gemini API để sinh câu trả lời dựa trên context được truy xuất
- **Kiểm soát hallucination** — yêu cầu rõ trong prompt: model phải nói "không tìm thấy" nếu thông tin không có trong tài liệu, thay vì bịa ra
- **Xử lý lỗi mềm** — bắt các lỗi từ API bên ngoài (ví dụ model quá tải) và trả về thông báo rõ ràng thay vì crash
- **Đóng gói Docker** — container hóa toàn bộ, đảm bảo chạy nhất quán trên nhiều môi trường

## Kiến trúc

```
Upload PDF
    │
    ▼
Trích xuất text (pypdf)
    │
    ▼
Chunking (sliding window có overlap)
    │
    ▼
Embedding + Lưu trữ (ChromaDB, kèm metadata document_name)
    │
    ▼
Câu hỏi user ──► Embed câu hỏi ──► Similarity Search (filter theo document_name)
                                          │
                                          ▼
                              Chunks liên quan + Câu hỏi
                                          │
                                          ▼
                                 Gemini API (generation)
                                          │
                                          ▼
                                    Câu trả lời
```

Toàn bộ flow trên được expose qua REST API bằng FastAPI và đóng gói bằng Docker.

## Công nghệ sử dụng

| Thành phần | Công nghệ |
|---|---|
| Ngôn ngữ | Python |
| LLM | Google Gemini API (`gemini-2.5-flash`) qua SDK `google-genai` |
| Vector Database | ChromaDB (local, persistent) |
| Đọc PDF | pypdf |
| API Framework | FastAPI |
| Đóng gói | Docker |

## Cài đặt & Chạy

### Yêu cầu
- Docker Desktop đã cài và đang chạy
- Gemini API key miễn phí từ [Google AI Studio](https://aistudio.google.com/apikey)

### Các bước

1. Clone repo
```bash
git clone https://github.com/hoangvanpierre/rag-chatbot-fastAPI.git
cd rag-chatbot-fastAPI
```

2. Tạo file `.env` ở thư mục gốc
```
GEMINI_API_KEY=your_key_here
```

3. Build Docker image
```bash
docker build -t rag-chatbot .
```

4. Chạy container
```bash
docker run -p 8000:8000 --env-file .env rag-chatbot
```

5. Mở giao diện API docs
```
http://127.0.0.1:8000/docs
```

## Các quyết định kỹ thuật đáng chú ý

- **Chunking có overlap**: text được chia thành các đoạn chồng lấp nhau, để thông tin nằm ở ranh giới giữa 2 chunk không bị mất khi retrieval.
- **Metadata filtering**: mỗi chunk được gắn tên tài liệu (`document_name`) ngay lúc lưu vào ChromaDB. Điều này tránh việc context từ các tài liệu khác nhau bị trộn lẫn khi có nhiều PDF cùng tồn tại trong vector store.
- **Instruction grounding rõ ràng**: prompt yêu cầu model thừa nhận khi không tìm thấy câu trả lời trong context, giảm hallucination.
- **Graceful degradation**: lỗi từ LLM API bên ngoài (ví dụ lỗi `503` quá tải) được bắt lại và trả về thông báo rõ ràng cho người dùng, thay vì lỗi `500` thô.

## Hướng cải thiện tiếp theo

- Hỗ trợ thêm các loại file khác (DOCX, TXT, ảnh qua OCR)
- Trả lời dạng streaming để giảm độ trễ cảm nhận
- Lưu lịch sử hội thoại / hỗ trợ hỏi nhiều lượt (multi-turn)
- Đổi sang embedding model dạng API để hỗ trợ đa ngôn ngữ tốt hơn
