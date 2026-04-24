from sqlalchemy import Column, String, Enum
from app.db.base import Base
import enum

class Status(str, enum.Enum):
    processing = "processing"
    completed = "completed"
    failed = "failed"

class Document(Base):
    __tablename__ = "documents"

    id = Column(String, primary_key=True)
    title = Column(String)
    status = Column(Enum(Status))