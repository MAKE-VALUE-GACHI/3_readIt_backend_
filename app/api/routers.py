from fastapi import APIRouter

from app.api.auth.controller import router as auth_router
from app.api.user.controller import router as user_router

api_router = APIRouter()

api_router.include_router(user_router)
api_router.include_router(auth_router)
