import os
import time
from google import genai
from dotenv import load_dotenv
from vector_store import search_similar_chunks
from google.genai import errors

load_dotenv()
client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])


def translate_to_english(text: str) -> str:
    """Dịch câu hỏi sang tiếng Anh để khớp ngôn ngữ với tài liệu khi retrieval"""
    
    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=f"Translate the following text to English. Only output the translation, nothing else.\n\nText: {text}"
        )
        return response.text.strip()
    except errors.APIError:
        # Nếu dịch lỗi, dùng tạm câu gốc
        return text

def build_rag_prompt(question: str, document_name: str = None, top_k: int = 3) -> str:
    
    question_for_search = translate_to_english(question)
    
    relevant_chunks = search_similar_chunks(question_for_search, top_k=top_k, document_name=document_name)
    context = "\n\n".join(relevant_chunks)
    
    prompt = f"""Dựa vào đoạn văn bản sau, hãy trả lời câu hỏi. 
Nếu thông tin không có trong đoạn văn bản, hãy nói "Tôi không tìm thấy thông tin này trong tài liệu."

Đoạn văn bản:
{context}

Câu hỏi: {question}

Trả lời:"""
    
    return prompt


def generate_answer_with_model(prompt: str, model_name: str) -> dict:
    """Gọi 1 model cụ thể, trả về answer + thời gian phản hồi"""
    
    start_time = time.time()
    
    try:
        response = client.models.generate_content(
            model=model_name,
            contents=prompt
        )
        answer = response.text
    except errors.ServerError:
        answer = "Hệ thống AI đang quá tải, vui lòng thử lại sau ít phút."
    except errors.APIError as e:
        answer = f"Đã có lỗi xảy ra khi gọi AI: {e.message}"
    
    elapsed = time.time() - start_time
    
    return {
        "model": model_name,
        "answer": answer,
        "response_time_seconds": round(elapsed, 2)
    }


def ask_question(question: str, document_name: str = None) -> str:
    
    prompt = build_rag_prompt(question, document_name)
    print("=" * 50)
    print("PROMPT GỬI ĐI:")
    print(prompt)
    print("=" * 50)
    
    result = generate_answer_with_model(prompt, model_name="gemini-2.5-flash")
    
    return result["answer"]


def compare_models(question: str, document_name: str = None) -> list[dict]:
    
    prompt = build_rag_prompt(question, document_name)
    
    models_to_test = ["gemini-2.5-flash", "gemini-2.5-flash-lite"]
    results = [generate_answer_with_model(prompt, model_name=m) for m in models_to_test]
    
    return results