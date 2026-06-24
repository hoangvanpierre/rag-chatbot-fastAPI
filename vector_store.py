import chromadb

client = chromadb.PersistentClient(path= "chrome_db")
collection = client.get_or_create_collection(name = "pdf_documents")

def add_chunks_to_db(chunks: list[str], document_name: str):
    """Thêm các chunk vào ChromaDB, kèm metadata document_name"""
    
    ids = [f"{document_name}_chunk_{i}" for i in range(len(chunks))]
    
    # Mỗi chunk có 1 dict metadata riêng, đánh dấu nó thuộc document nào
    metadatas = [{"document_name": document_name} for _ in chunks]
    
    collection.add(
        documents=chunks,
        ids=ids,
        metadatas=metadatas   # Thêm dòng này
    )
    
    print(f"Đã thêm {len(chunks)} chunks vào ChromaDB cho document '{document_name}'")


def search_similar_chunks(query: str, top_k: int = 3, document_name: str = None) -> list[str]:
    """
    Tìm top_k chunks giống nhất với câu query.
    Nếu document_name được truyền vào, chỉ tìm trong chunks của document đó.
    """
    
    where_filter = {"document_name": document_name} if document_name else None
    
    results = collection.query(
        query_texts=[query],
        n_results=top_k,
        where=where_filter   # ChromaDB chỉ tìm trong các chunk khớp filter này
    )
    
    return results["documents"][0]
