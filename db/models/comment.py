# app/db/models/comment.py
from beanie import Document
from datetime import datetime

class Comment(Document):
    answer_id: str  # Reference to the Answer
    comment: str
    user_id: str  # User who made the comment
    created_at: datetime = datetime.now()

    class Settings:
        name = "comments"
