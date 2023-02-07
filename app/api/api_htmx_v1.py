from fastapi import APIRouter

from app.api.api_htmx import page_index, food

htmx_router = APIRouter()

htmx_router.include_router(page_index.router)
htmx_router.include_router(food.router, prefix="/food")