from fastapi import APIRouter

from app.api.auth.controller import router as auth_router
from app.api.category.controller import router as category_router
from app.api.comment.controller import router as comment_router
from app.api.scrap.controller import router as scrap_router
from app.api.user.controller import router as user_router

api_router = APIRouter()

api_router.include_router(user_router)
api_router.include_router(auth_router)

api_router.include_router(scrap_router)
api_router.include_router(category_router)
api_router.include_router(comment_router)
