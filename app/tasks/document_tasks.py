from app.tasks.worker import celery
from app.services.document_service import process_document_pipeline

@celery.task (name="app.tasks.document_tasks.process_document_task")
def process_document_task(doc_id: str, file_path: str):
    return process_document_pipeline(doc_id, file_path)