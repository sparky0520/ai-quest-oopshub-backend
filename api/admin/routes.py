# app/api/admin_routes.py
from fastapi import APIRouter, Depends, HTTPException, status
from db.models.user import User
from db.models.company import Company
from utils.dependencies import verify_admin_access

router = APIRouter()

@router.get("/access-requests")
async def get_access_requests( 
    current_user: User = Depends(verify_admin_access)
):
    company_id = current_user.company_id
    pending_users = await User.find(User.company_id == company_id, User.status == "pending").to_list()

    # only return necessary fields
    pending_users = [
        {
            "id": str(user.id),
            "name": user.name,
            "email": user.email,
        }
        for user in pending_users
    ]

    return {"access_requests": pending_users}

@router.post("/manage-user")
async def manage_user(
    action_data: dict,
    current_user: User = Depends(verify_admin_access)
):
    company_id = current_user.company_id
    user = await User.get(action_data["user_id"])
    if not user or user.company_id != company_id:
        raise HTTPException(status_code=404, detail="User not found or not in company")

    action = action_data["action"]
    if action == "approve":
        user.status = "joined"
        user.role = action_data.get("role", "employee")
    elif action == "reject":
        user.company_id = None
        user.status = "pending"
    elif action == "block":
        user.status = "blocked"
    else:
        raise HTTPException(status_code=400, detail="Invalid action")
    
    await user.save()
    return {"message": f"User {action}ed successfully"}

@router.patch("/users/{user_id}/role")
async def update_user_role(
    user_id: str, 
    role_data: dict,
    current_user: User = Depends(verify_admin_access)
):
    company_id = current_user.company_id
    user = await User.get(user_id)
    if not user or user.company_id != company_id:
        raise HTTPException(status_code=404, detail="User not found or not in company")

    user.role = role_data["role"]
    await user.save()
    return {"message": "User role updated successfully"}
