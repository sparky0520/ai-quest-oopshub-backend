# app/api/admin_routes.py
from fastapi import APIRouter, Depends, HTTPException, status
from db.models.user import User
from db.models.company import Company
from utils.dependencies import verify_admin_access

router = APIRouter()

@router.get("/companies/{company_id}/access-requests")
async def get_access_requests(
    company_id: str, 
    current_user: User = Depends(verify_admin_access)
):
    pending_users = await User.find(User.company_id == company_id, User.status == "pending").to_list()
    return {"access_requests": pending_users}

@router.post("/companies/{company_id}/manage-user")
async def manage_user(
    company_id: str, 
    action_data: dict,
    current_user: User = Depends(verify_admin_access)
):
    user = await User.get(action_data["user_id"])
    if not user or user.company_id != company_id:
        raise HTTPException(status_code=404, detail="User not found or not in company")

    action = action_data["action"]
    if action == "approve":
        user.status = "joined"
        user.role = action_data.get("role", "user")
    elif action == "reject":
        user.company_id = None
        user.status = "pending"
    elif action == "block":
        user.status = "blocked"
    else:
        raise HTTPException(status_code=400, detail="Invalid action")
    
    await user.save()
    return {"message": f"User {action}ed successfully"}

@router.patch("/companies/{company_id}/users/{user_id}/role")
async def update_user_role(
    company_id: str, 
    user_id: str, 
    role_data: dict,
    current_user: User = Depends(verify_admin_access)
):
    user = await User.get(user_id)
    if not user or user.company_id != company_id:
        raise HTTPException(status_code=404, detail="User not found or not in company")

    user.role = role_data["role"]
    await user.save()
    return {"message": "User role updated successfully"}
