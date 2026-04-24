from fastapi import APIRouter, UploadFile, File, Form
import uuid

router = APIRouter()

@router.post("/upload")
async def upload_document(file: UploadFile = File(...), title: str = Form(...)):
    doc_id = str(uuid.uuid4())

    # Save file locally
    with open(f"data/{doc_id}_{file.filename}", "wb") as f:
        f.write(await file.read())

    return {
        "document_id": doc_id,
        "status": "processing"
    }