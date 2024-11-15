# app/db/models/question.py
from beanie import Document
from datetime import datetime
from typing import List

class Question(Document):
    title: str
    description: str
    tags: List[str] = []
    user_id: str  # User who asked the question\
    company_id: str  # Company to which the question belongs
    upvotes: int = 0
    created_at: datetime = datetime.now()
    updated_at: datetime = datetime.now()

    class Settings:
        name = "questions"
