from fastapi import APIRouter
from app.api.v1.routes.analytics import router as analytics_router
from app.api.v1.routes.createUser import router as create_user
from app.api.v1.routes.auth import router as auth_router

api_router = APIRouter()

api_router.include_router(analytics_router, prefix="/analytics", tags=["Analytics"])
api_router.include_router(create_user, prefix="/users", tags=["Users"])
api_router.include_router(auth_router, prefix="/auth", tags=["Auth"])