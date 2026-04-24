from fastapi import FastAPI
from app.api.routes import documents, qa

app = FastAPI(title="Smart Document Q&A")

app.include_router(documents.router, prefix="/api/v1/documents")
app.include_router(qa.router, prefix="/api/v1/qa")