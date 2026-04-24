from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import os
import pickle

model = SentenceTransformer("all-MiniLM-L6-v2")

INDEX_DIR = "data/indices"
os.makedirs(INDEX_DIR, exist_ok=True)

def store_vectors(doc_id, chunks):
    embeddings = model.encode(chunks)

    dim = embeddings.shape[1]
    index = faiss.IndexFlatIP(dim)

    index.add(np.array(embeddings))

    # Save index
    faiss.write_index(index, f"{INDEX_DIR}/{doc_id}.index")

    # Save chunks
    with open(f"{INDEX_DIR}/{doc_id}.pkl", "wb") as f:
        pickle.dump(chunks, f)