from fastapi import APIRouter
from backend.api import health, offline, ui
api_router = APIRouter()
api_router.include_router(health.router, tags=["health"])
api_router.include_router(offline.router, prefix="/api", tags=["offline"])
api_router.include_router(ui.router, tags=["ui"])
