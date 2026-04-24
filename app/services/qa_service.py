import os
import faiss
import pickle
import numpy as np
from sentence_transformers import SentenceTransformer
from fastapi.concurrency import run_in_threadpool
from app.services.llm_service import llm_service

INDEX_DIR = "data/indices"

model = SentenceTransformer("all-MiniLM-L6-v2")


# -----------------------------
# LOAD INDEX
# -----------------------------
def load_index(document_id: str):
    index_path = f"{INDEX_DIR}/{document_id}.index"
    chunks_path = f"{INDEX_DIR}/{document_id}.pkl"

    if not os.path.exists(index_path) or not os.path.exists(chunks_path):
        raise FileNotFoundError(f"Index not found for {document_id}")

    index = faiss.read_index(index_path)

    with open(chunks_path, "rb") as f:
        chunks = pickle.load(f)

    return index, chunks


# -----------------------------
# RETRIEVAL
# -----------------------------
def retrieve_context(document_id: str, question: str, k: int = 4):
    index, chunks = load_index(document_id)

    query_vec = model.encode([question]).astype("float32")

    # IMPORTANT: only valid if index was also normalized during ingestion
    faiss.normalize_L2(query_vec)

    scores, indices = index.search(query_vec, k)

    results = []
    sources = []

    for idx in indices[0]:
        idx = int(idx)  # ✅ FIX numpy.int64 issue

        if 0 <= idx < len(chunks):
            results.append(chunks[idx])
            sources.append(idx)

    return "\n\n".join(results), sources


# -----------------------------
# LLM
# -----------------------------
def generate_answer(context: str, question: str):
    if not context.strip():
        return "I don't know based on the document."

    return llm_service.generate(context, question)


# -----------------------------
# SAFE TRUNCATION (sentence safe)
# -----------------------------
def safe_truncate(text: str, max_chars: int = 800):
    if len(text) <= max_chars:
        return text
    return text[:max_chars].rsplit(".", 1)[0] + "."


# -----------------------------
# ORCHESTRATOR
# -----------------------------
async def answer_question(req):
    try:
        context, sources = await run_in_threadpool(
            retrieve_context,
            req.document_id,
            req.question
        )

        if not context:
            return {
                "document_id": req.document_id,
                "question": req.question,
                "answer": "I don't know based on the document.",
                "sources": []
            }

        answer = await run_in_threadpool(
            generate_answer,
            context,
            req.question
        )

        return {
            "document_id": str(req.document_id),
            "question": str(req.question),
            "answer": str(answer),
            "sources": [int(s) for s in sources],  # 🔥 final safety
            "context_used": safe_truncate(context)
        }

    except Exception as e:
        return {
            "document_id": req.document_id,
            "question": req.question,
            "answer": f"System error: {str(e)}",
            "sources": []
        }