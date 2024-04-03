from fastapi import APIRouter

from src.services.auth.views import router as auth_router
from src.services.users.views import router as users_router

router = APIRouter()
router.include_router(auth_router)
router.include_router(users_router)

