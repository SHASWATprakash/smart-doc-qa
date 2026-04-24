from app.utils.parser import parse_pdf, parse_docx
from app.utils.chunker import chunk_text
from app.services.vector_store import store_vectors
import os

def process_document_pipeline(doc_id: str, file_path: str):
    # 1. Extract text
    if file_path.endswith(".pdf"):
        text = parse_pdf(file_path)
    else:
        text = parse_docx(file_path)

    # 2. Chunk text
    chunks = chunk_text(text)

    # 3. Store embeddings in FAISS
    store_vectors(doc_id, chunks)

    return {
        "doc_id": doc_id,
        "chunks": len(chunks),
        "status": "indexed"
    }