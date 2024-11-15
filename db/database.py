# app/db/database.py
from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient
from .models.user import User
from .models.company import Company
from core.config import settings

async def init_db():
    client = AsyncIOMotorClient(settings.MONGODB_URI)
    await init_beanie(database=client.oopshub, document_models=[User, Company])
