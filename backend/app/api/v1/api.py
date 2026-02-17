# app/api/v1/api.py
from fastapi import APIRouter
from app.api.v1.endpoints import auth, users, transactions, analytics, goals

api_router = APIRouter()

# Existing routers...
api_router.include_router(auth.router, tags=["login"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(transactions.router, prefix="/transactions", tags=["transactions"])

api_router.include_router(analytics.router, prefix="/analytics", tags=["analytics"])

# NEW: Add the goals router
api_router.include_router(goals.router, prefix="/goals", tags=["goals"])