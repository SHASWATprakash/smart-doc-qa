📄 Smart Document Q&A System
A production-grade API that lets users upload documents (PDF/DOCX) and ask natural language questions answered using retrieval-augmented generation (RAG).
🚀 Quick Start
bashgit clone <https://github.com/SHASWATprakash/smart-doc-qa>
cd smart-doc-qa
cp .env.example .env   # Fill in your OPENAI_API_KEY
docker-compose up --build
API is live at http://localhost:8000
Docs at http://localhost:8000/docs

📡 Sample API Calls
1. Upload a Document
bashcurl -X POST http://localhost:8000/api/v1/documents/upload \
  -F "file=@sample_docs/machine_learning.pdf" \
  -F "title=ML Overview"
Response:
json{
  "document_id": "abc123",
  "status": "processing",
  "task_id": "celery-task-xyz"
}
2. Check Processing Status
bashcurl http://localhost:8000/api/v1/documents/abc123/status
3. Ask a Question
bashcurl -X POST http://localhost:8000/api/v1/qa/ask \
  -H "Content-Type: application/json" \
  -d '{
    "document_id": "abc123",
    "question": "What is supervised learning?",
    "conversation_id": null
  }'
4. Follow-up Question (same conversation)
bashcurl -X POST http://localhost:8000/api/v1/qa/ask \
  -H "Content-Type: application/json" \
  -d '{
    "document_id": "abc123",
    "question": "Can you give me an example of that?",
    "conversation_id": "conv-xyz"
  }'
5. List Documents
bashcurl http://localhost:8000/api/v1/documents/

🧠 Design Decisions
Chunking Strategy
Why overlapping chunks?
Documents are split into 512-token chunks with a 64-token overlap. The overlap ensures that sentences split at chunk boundaries don't lose context. I chose 512 tokens because it fits well within embedding model limits while being large enough to contain a complete thought.
Why not split by paragraphs?
Paragraphs vary wildly in length. A 5-word paragraph and a 2000-word section would both be "one chunk." Fixed-size chunking with overlap gives consistent retrieval quality.
Embedding Model
I use sentence-transformers/all-MiniLM-L6-v2 — it's fast (14,000 sentences/sec on CPU), small (80MB), and produces high-quality 384-dim embeddings. For production, you'd swap to text-embedding-3-small (OpenAI) for better quality at low cost.
Vector Search: FAISS
FAISS runs in-process (no separate service), uses IndexFlatIP (inner product / cosine similarity after normalization), and is fast enough for thousands of documents. For scale, you'd migrate to Pinecone or pgvector. FAISS indices are persisted to disk per document.
Async Design
Document uploads return immediately with a task_id. Celery + Redis handles the heavy work (text extraction, chunking, embedding) in the background. Clients poll /documents/{id}/status to check progress. This means a 50MB PDF never blocks the API.
Conversation Handling
Each Q&A session gets a conversation_id. The last 5 exchanges are stored in the DB and prepended to the LLM prompt, giving the model conversation context. This enables follow-up questions like "Can you explain that in simpler terms?" to work correctly.
Failure Handling

OpenAI down: Returns 503 with a clear message. The question and retrieved chunks are logged so you can retry without re-fetching.
Corrupt document: The Celery task catches extraction errors, marks document as failed, and stores the error message.
Answer not in document: The prompt explicitly instructs the LLM to say "I don't know based on the provided document" rather than hallucinate.
Empty FAISS results: Falls back gracefully with a "no relevant content found" response.

Why SQLAlchemy + Alembic?
Schema migrations matter. Alembic gives us a versioned, reproducible schema history. SQLAlchemy's async support (asyncpg) keeps the API non-blocking.

🗂️ Project Structure
smart-doc-qa/
├── app/
│   ├── api/routes/          # FastAPI route handlers
│   ├── core/                # Config, settings
│   ├── db/                  # Database session, base
│   ├── models/              # SQLAlchemy ORM models
│   ├── schemas/             # Pydantic request/response schemas
│   ├── services/            # Business logic (document, QA, vector)
│   ├── tasks/               # Celery tasks
│   └── utils/               # PDF/DOCX parsers, chunker, embedder
├── alembic/                 # DB migrations
├── sample_docs/             # 3 sample documents for testing
├── docker-compose.yml
├── Dockerfile
└── .env.example

🔧 Environment Variables
See .env.example for all required variables.
VariableDescriptionOPENAI_API_KEYYour OpenAI API keyDATABASE_URLPostgreSQL connection stringREDIS_URLRedis connection stringFAISS_INDEX_PATHDirectory to store FAISS indices

🧪 Running Tests
bashdocker-compose exec api pytest tests/ -v