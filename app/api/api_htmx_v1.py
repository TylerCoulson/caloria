from fastapi import APIRouter

from app.api.api_htmx import daily_overview, page_index, food, serving_size, profile, food_log, predictions
from app.auth.html_routers import validation, page_routers, verification, forgot_password

htmx_router = APIRouter(include_in_schema=False, tags=['htmx'])

htmx_router.include_router(page_index.router, tags=['htmx-index'])
htmx_router.include_router(food.router, tags=['htmx-food'])
htmx_router.include_router(profile.router, tags=['htmx-profile'])
# htmx_router.include_router(serving_size.router, tags=['htmx-servings'])
htmx_router.include_router(daily_overview.router, tags=['htmx-daily'])
htmx_router.include_router(food_log.router, tags=['htmx-food_log'])
htmx_router.include_router(predictions.router, tags=['htmx-prediction'])
htmx_router.include_router(page_routers.router, tags=['htmx-auth-pages'])
htmx_router.include_router(validation.router, tags=['htmx-validation'])
htmx_router.include_router(verification.router, tags=['htmx-verification'])
htmx_router.include_router(forgot_password.router, tags=['htmx-reset-password'])