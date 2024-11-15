# app/main.py
from fastapi import FastAPI
from db.database import init_db
from api.auth import routes as auth_routes
from api.companies import routes as companies_routes
from api.admin import routes as admin_routes

app = FastAPI()

@app.on_event("startup")
async def startup_event():
    await init_db()

app.include_router(auth_routes.router, prefix="/auth", tags=["Authentication"])
app.include_router(companies_routes.router, prefix="/companies", tags=["Companies"])
app.include_router(admin_routes.router, prefix="/admin", tags=["Admin"])
