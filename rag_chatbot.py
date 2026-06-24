import os
from google import genai
from dotenv import load_dotenv
from vector_store import search_similar_chunks
from google.genai import errors

load_dotenv()
client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

def ask_question(question: str, document_name: str = None) -> str:
    relevant_chunks = search_similar_chunks(question, top_k=3, document_name=document_name)
    context = "\n\n".join(relevant_chunks)
    
    prompt = f"""Dựa vào đoạn văn bản sau, hãy trả lời câu hỏi. 
Nếu thông tin không có trong đoạn văn bản, hãy nói "Tôi không tìm thấy thông tin này trong tài liệu."

Đoạn văn bản:
{context}

Câu hỏi: {question}

Trả lời:"""
    
    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )
        return response.text
    except errors.ServerError:
        return "Hệ thống AI đang quá tải, vui lòng thử lại sau ít phút."
    except errors.APIError as e:
        return f"Đã có lỗi xảy ra khi gọi AI: {e.message}"