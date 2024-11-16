# app/utils/dependencies.py
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from db.models.user import User
from core.security import verify_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

async def verify_user(token: str = Depends(oauth2_scheme)):
    payload = verify_token(token)
    if payload is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    return payload

async def get_current_user(token: str = Depends(verify_user)):
    user_id = token.get("sub")
    if not user_id:
        raise HTTPException(status_code=401, detail="Unauthorized")
    user = await User.get(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


async def verify_admin_access(token: str = Depends(verify_user)):
    user_id = token.get("sub")
    if not user_id:
        raise HTTPException(status_code=401, detail="Unauthorized")

    user = await User.get(user_id)
    if not user or user.role not in ["admin", "hr"]:
        raise HTTPException(status_code=403, detail="Forbidden: Admin access required")
    return user

async def verify_in_company(token: str = Depends(verify_user)):
    user_id = token.get("sub")
    if not user_id:
        raise HTTPException(status_code=401, detail="Unauthorized")

    user = await User.get(user_id)
    if not user or not user.company_id or user.status != "joined":
        raise HTTPException(status_code=403, detail="Forbidden: User not part of a company")
    return user