from fastapi import APIRouter

from app.api.api_htmx import daily_overview, page_index, food, serving_size, user, food_log, get_posting_html

htmx_router = APIRouter()

htmx_router.include_router(page_index.router)
htmx_router.include_router(food.router, prefix="/food")
htmx_router.include_router(user.router, prefix="/user")
htmx_router.include_router(serving_size.router, prefix="/servings")
htmx_router.include_router(daily_overview.router, prefix="/daily")
htmx_router.include_router(food_log.router, prefix="/food_log")
htmx_router.include_router(get_posting_html.router, prefix="/create")