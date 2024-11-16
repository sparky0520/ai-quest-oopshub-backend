from fastapi import APIRouter, Depends, HTTPException
from db.models.company import Company
from db.models.user import User
from utils.dependencies import get_current_user

router = APIRouter(prefix="/users", tags=["Users"])

@router.get("/me")
async def verify_user(current_user: User = Depends(get_current_user)):

    # Select the fields to return
    user = {
        "email": current_user.email,
        "name": current_user.name,
        "role": current_user.role,
        "company_id": current_user.company_id,
        "status": current_user.status,
    }
    return user