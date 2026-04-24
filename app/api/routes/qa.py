from fastapi import APIRouter
from pydantic import BaseModel
from app.services.qa_service import answer_question

router = APIRouter()

class QuestionRequest(BaseModel):
    document_id: str
    question: str
    conversation_id: str | None = None

@router.post("/ask")
async def ask(req: QuestionRequest):
    return await answer_question(req)