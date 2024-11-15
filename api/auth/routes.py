# app/api/auth/routes.py
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, EmailStr
from db.models.user import User
from core.security import create_access_token, hash_password, verify_password
from db.database import init_db

router = APIRouter()

class UserRegister(BaseModel):
    email: EmailStr
    password: str
    name: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

@router.post("/register", status_code=201)
async def register_user(user: UserRegister):
    existing_user = await User.find_one(User.email == user.email)
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    hashed_password = hash_password(user.password)
    new_user = User(email=user.email, password=hashed_password, name=user.name)
    await new_user.insert()
    return {"message": "User registered successfully"}

@router.post("/login")
async def login_user(user: UserLogin):
    db_user = await User.find_one(User.email == user.email)
    if not db_user or not verify_password(user.password, db_user.password):
        raise HTTPException(status_code=400, detail="Invalid credentials")
    token = create_access_token({"sub": str(db_user.id)})
    return {"access_token": token, "token_type": "bearer"}
