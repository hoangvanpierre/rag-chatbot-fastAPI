from pdf_processor import extract_text_from_pdf, chunk_text
from vector_store import add_chunks_to_db, search_similar_chunks

#text = extract_text_from_pdf(r"data\Choice True Visualization.pdf")
#chunks = chunk_text(text)

#add_chunks_to_db(chunks, document_name="ai_math_paper")
results = search_similar_chunks("Biểu đồ tròn có tác dụng gì?", top_k=5)

for i, chunk in enumerate(results):
    print(f"\n--- Kết quả {i+1} ---")
    print(chunk[:500])