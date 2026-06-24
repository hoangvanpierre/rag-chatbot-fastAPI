from pdf_processor import extract_text_from_pdf, chunk_text

text = extract_text_from_pdf(r"data\The mathematics of AI Paper.pdf")
print("Tổng số ký tự:", len(text))

chunks = chunk_text(text)
print("Số lượng chunks:", len(chunks))
print("\n--- Chunk đầu tiên ---")
print(chunks[0])
print("\n--- Chunk thứ hai ---")
print(chunks[1])