import numpy as np
from app.vector.embedder import embedder
from app.vector.faiss_store import faiss_store

class RetrievalService:

    def get_context(self, document_id: str, question: str, k: int = 5):

        index, chunks = faiss_store.load(document_id)

        query_vec = embedder.encode([question])
        scores, indices = faiss_store.search(index, query_vec, k)

        results = []
        for score, i in zip(scores[0], indices[0]):
            if 0 <= i < len(chunks) and score > 0.3:
                results.append(chunks[i])

        return "\n\n".join(results)

retrieval_service = RetrievalService()