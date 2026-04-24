from fastapi import APIRouter, UploadFile, File, Form
import uuid
import os
from app.tasks.document_tasks import process_document_task

router = APIRouter()

UPLOAD_DIR = "/app/data/uploads"

os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/upload")
async def upload_document(file: UploadFile = File(...), title: str = Form(...)):
    doc_id = str(uuid.uuid4())

    file_path = f"{UPLOAD_DIR}/{doc_id}_{file.filename}"

    with open(file_path, "wb") as f:
        f.write(await file.read())

  
    process_document_task.delay(doc_id, file_path)

    return {
        "document_id": doc_id,
        "status": "processing"
    }