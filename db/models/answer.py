from beanie import Document
from datetime import datetime
from typing import Optional

class Answer(Document):
    question_id: str  # Reference to the Question
    answer: str
    user_id: Optional[str]  # User who answered; None if AI-generated
    upvotes: int = 0
    is_ai: bool = False  # Flag to indicate if the answer is AI-generated
    created_at: datetime = datetime.now()
    updated_at: datetime = datetime.now()

    class Settings:
        name = "answers"
