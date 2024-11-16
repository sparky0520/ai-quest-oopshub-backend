# app/main.py
from fastapi import FastAPI
from db.database import init_db
from fastapi.middleware.cors import CORSMiddleware
from api.auth import routes as auth_routes
from api.companies import routes as companies_routes
from api.admin import routes as admin_routes
from api.questions import routes as questions_routes
from api.questions import voting_routes
from api.users import routes as users_routes

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup_event():
    await init_db()

app.include_router(auth_routes.router, prefix="/auth", tags=["Authentication"])
app.include_router(companies_routes.router, prefix="/companies", tags=["Companies"])
app.include_router(admin_routes.router, prefix="/admin", tags=["Admin"])
app.include_router(questions_routes.router)
app.include_router(voting_routes.router)
app.include_router(users_routes.router)