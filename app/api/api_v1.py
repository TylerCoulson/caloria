from fastapi import APIRouter
from app.api.api_V1 import daily_overview, food_log, food, serving_size, profile, recipe, predictions, food_cats
from app.auth.router import auth_router

api_router = APIRouter(prefix="/api/v1")
api_router.include_router(food.router, prefix="/food")
# api_router.include_router(food_cats.router, prefix="/food-cats")
api_router.include_router(food_log.router, prefix="/food_log", tags=["food_log"])
api_router.include_router(profile.router, prefix="/profile", tags=["profile"])
# api_router.include_router(recipe.router, prefix="/recipe", tags=["recipe"])
# api_router.include_router(daily_overview.router, prefix="/daily", tags=["daily"])
# api_router.include_router(predictions.router, prefix="/predictions", tags=["predictions"])
api_router.include_router(auth_router, tags=['auth'])