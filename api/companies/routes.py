# app/api/companies/routes.py
from fastapi import APIRouter, Depends, HTTPException
from db.models.company import Company
from db.models.user import User
from utils.dependencies import get_current_user

router = APIRouter()

@router.get("/", dependencies=[Depends(get_current_user)])
async def list_companies():
    companies = await Company.all().to_list()
    return companies

@router.post("/")
async def create_company(company_data: dict, current_user: dict = Depends(get_current_user)):
    current_user_doc = await User.get(current_user["sub"])
    if current_user_doc is None:
        print(current_user["sub"])
        raise HTTPException(status_code=404, detail="User not found")

    if current_user_doc.company_id:
        raise HTTPException(status_code=400, detail="User is already part of a company")
    
    new_company = Company(
        name=company_data["name"],
        admin_user_id=str(current_user_doc.id),
        ai_answer_enabled=company_data.get("ai_answer_enabled", True)
    )
    await new_company.insert()
    
    current_user_doc.company_id = str(new_company.id)
    current_user_doc.status = "joined"
    current_user_doc.role = "admin"
    await current_user_doc.save()

    return {"message": "Company created successfully", "company_id": str(new_company.id)}

@router.patch("/{company_id}")
async def update_company(company_id: str, update_data: dict, current_user: dict = Depends(get_current_user)):
    company = await Company.get(company_id)
    if not company or company.admin_user_id != current_user["sub"]:
        raise HTTPException(status_code=403, detail="Access denied")

    if "name" in update_data:
        company.name = update_data["name"]
    if "ai_answer_enabled" in update_data:
        company.ai_answer_enabled = update_data["ai_answer_enabled"]
    
    await company.save()
    return {"message": "Company details updated successfully"}

@router.get("/{company_id}")
async def get_company_details(company_id: str):
    company = await Company.get(company_id)
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")
    return company

@router.post("/{company_id}/access-request")
async def request_access(company_id: str, current_user: dict = Depends(get_current_user)):
    company = await Company.get(company_id)
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")
    
    current_user_doc = await User.get(current_user["sub"])
    if current_user_doc.status == "joined":
        raise HTTPException(status_code=400, detail="User already part of a company")
    
    current_user_doc.company_id = company_id
    current_user_doc.status = "pending"
    await current_user_doc.save()
    return {"message": "Access request sent. Please wait for HR approval."}
