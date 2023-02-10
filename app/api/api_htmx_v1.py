from fastapi import APIRouter

from app.api.api_htmx import page_index, food, serving_size, user, daily_output

htmx_router = APIRouter()

htmx_router.include_router(page_index.router)
htmx_router.include_router(food.router, prefix="/food")
htmx_router.include_router(user.router, prefix="/user")
htmx_router.include_router(serving_size.router, prefix="/servings")
htmx_router.include_router(daily_output.router, prefix="/daily")