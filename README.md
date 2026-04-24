# 📄 Smart Document Q&A System

A **production-grade Retrieval-Augmented Generation (RAG) system** that allows users to upload documents (PDF/DOCX) and ask natural language questions answered using semantic search + LLM reasoning.

---

## 🚀 Features

- 📤 Upload PDF / DOCX documents
- 🧠 Async document processing with Celery + Redis
- 🔍 Semantic search using FAISS vector index
- 🤖 LLM-powered question answering (context-aware)
- 💬 Conversation support via conversation_id
- ⚡ Fast API with FastAPI + Uvicorn
- 🐳 Fully Dockerized (API + Worker + DB + Redis)
- 🧩 Modular architecture (services, tasks, utils)

---

## 🚀 Quick Start

```bash
git clone https://github.com/SHASWATprakash/smart-doc-qa
cd smart-doc-qa

cp .env.example .env   # Add OPENAI_API_KEY

docker-compose up --build


API: http://localhost:8000

Docs: http://localhost:8000/docs

📡 API Usage
1️⃣ Upload Document
curl -X POST http://localhost:8000/api/v1/documents/upload \
  -F "file=@sample_docs/machine_learning.pdf" \
  -F "title=ML Overview"

Response:

{
  "document_id": "abc123",
  "status": "processing",
  "task_id": "celery-task-xyz"
}
2️⃣ Check Processing Status
curl http://localhost:8000/api/v1/documents/abc123/status
3️⃣ Ask Question
curl -X POST http://localhost:8000/api/v1/qa/ask \
  -H "Content-Type: application/json" \
  -d '{
    "document_id": "abc123",
    "question": "What is supervised learning?",
    "conversation_id": null
  }'
4️⃣ Follow-up Question
curl -X POST http://localhost:8000/api/v1/qa/ask \
  -H "Content-Type: application/json" \
  -d '{
    "document_id": "abc123",
    "question": "Give an example",
    "conversation_id": "conv-xyz"
  }'
🧠 Architecture
🔄 RAG Pipeline
Upload PDF
   ↓
Celery Task
   ↓
Text Extraction
   ↓
Chunking (512 tokens + overlap)
   ↓
Embedding (MiniLM)
   ↓
FAISS Index Storage
   ↓
Query → Retrieval → LLM Answer
🧩 Design Decisions
📌 Chunking
Fixed-size 512-token chunks
64-token overlap
Ensures context continuity
📌 Embeddings
sentence-transformers/all-MiniLM-L6-v2
Fast CPU inference
384-dimensional embeddings
📌 Vector Store
FAISS IndexFlatIP (cosine similarity)
Stored per document
Future-ready for pgvector/Pinecone
📌 Async Processing
Celery + Redis for background ingestion
Non-blocking API design
📌 Conversation Memory
conversation_id tracks last interactions
Enables follow-up question handling
🗂️ Project Structure
smart-doc-qa/
├── app/
│   ├── api/routes/
│   ├── core/
│   ├── db/
│   ├── models/
│   ├── schemas/
│   ├── services/
│   ├── tasks/
│   └── utils/
├── alembic/
├── sample_docs/
├── docker-compose.yml
├── Dockerfile
└── .env.example
🔧 Environment Variables
Variable	Description
OPENAI_API_KEY	OpenAI API key
DATABASE_URL	PostgreSQL connection
REDIS_URL	Redis connection
FAISS_INDEX_PATH	Vector storage path


🧪 Run Tests
docker-compose exec api pytest tests/ -v