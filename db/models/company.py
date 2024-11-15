# app/db/models/company.py
from beanie import Document
from pydantic import BaseModel
from typing import Optional

class Company(Document):
    name: str
    admin_user_id: str  # The ID of the admin (e.g., an HR user)
    ai_answer_enabled: bool = True  # Toggle for AI-generated answers

    class Settings:
        collection = "companies"  # MongoDB collection name