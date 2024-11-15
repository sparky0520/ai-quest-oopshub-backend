# app/db/models/user.py
from beanie import Document
from pydantic import BaseModel, EmailStr
from typing import Optional

class User(Document):
    email: EmailStr
    password: str
    name: str
    company_id: Optional[str] = None  # References the user's company (if joined)
    status: str = "pending"  # Possible values: "pending", "joined"
    role: str = "user"  # Default role, e.g., "admin", "hr", "employee"

    class Settings:
        collection = "users"
