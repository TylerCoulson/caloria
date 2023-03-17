from fastapi import APIRouter

from app.api.api_htmx import daily_overview, page_index, food, serving_size, profile, food_log, get_posting_html, predictions
from app.auth.html_routers import validation, page_routers

htmx_router = APIRouter(include_in_schema=False)

htmx_router.include_router(page_index.router, tags=['htmx-index'])
htmx_router.include_router(food.router, tags=['htmx-food'])
htmx_router.include_router(profile.router, tags=['htmx-profile'])
htmx_router.include_router(serving_size.router, prefix="/servings", tags=['htmx-servings'])
htmx_router.include_router(daily_overview.router, prefix="/daily", tags=['htmx-daily'])
htmx_router.include_router(food_log.router, prefix="/food_log", tags=['htmx-food_log'])
htmx_router.include_router(get_posting_html.router, tags=['htmx-create'])
htmx_router.include_router(predictions.router, tags=['htmx-prediction'])
htmx_router.include_router(page_routers.router, tags=['htmx-auth-pages'])
htmx_router.include_router(validation.router, tags=['htmx-validation'])