from fastapi import APIRouter

from app.api.user.controller import router as user_router
from app.api.scrap.controller import router as scrap_router

api_router = APIRouter()

api_router.include_router(user_router)

api_router.include_router(scrap_router)