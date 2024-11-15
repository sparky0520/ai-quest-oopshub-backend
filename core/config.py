# app/core/config.py
import os
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    JWT_SECRET: str = os.getenv("JWT_SECRET", "your-secret-key")
    MONGODB_URI: str = os.getenv("MONGODB_URI", "mongodb://localhost:27017")

settings = Settings()