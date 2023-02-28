from fastapi import APIRouter

from app.api.api_htmx import daily_overview, page_index, food, serving_size, user, food_log, get_posting_html, predictions

htmx_router = APIRouter()

htmx_router.include_router(page_index.router, tags=['htmx-index'])
htmx_router.include_router(food.router, prefix="/food", tags=['htmx-food'])
htmx_router.include_router(user.router, prefix="/user", tags=['htmx-user'])
htmx_router.include_router(serving_size.router, prefix="/servings", tags=['htmx-servings'])
htmx_router.include_router(daily_overview.router, prefix="/daily", tags=['htmx-daily'])
htmx_router.include_router(food_log.router, prefix="/food_log", tags=['htmx-food_log'])
htmx_router.include_router(get_posting_html.router, prefix="/create", tags=['htmx-create'])
htmx_router.include_router(predictions.router, prefix="/prediction", tags=['htmx-prediction'])