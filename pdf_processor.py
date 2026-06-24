import pypdf

def extract_text_from_pdf(file_path: str):
    reader = pypdf.PdfReader(file_path)
    full_text = ""

    for page in reader.pages:
        page_text = page.extract_text()
        full_text += page_text + "\n"
    return full_text

def chunk_text(text: str, chunk_size: int = 500, overlap: int = 50) -> list[str]:
    
    chunks = []
    step = chunk_size - overlap

    for i in range(0, len(text), step):
        chunk = text[i : i + chunk_size]
        chunks.append(chunk)

        if i + chunk_size >= len(text):
            break
    return chunks