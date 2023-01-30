from fastapi import APIRouter
from app.api.api_V1 import food_log, food, serving_size, user, recipe

api_router = APIRouter()
api_router.include_router(food.router, prefix="/food", tags=["food"])
api_router.include_router(food_log.router, prefix="/food_log", tags=["food_log"])
api_router.include_router(serving_size.router, prefix="/serving_size", tags=["serving_size"])
api_router.include_router(user.router, prefix="/user", tags=["user"])
api_router.include_router(recipe.router, prefix="/recipe", tags=["recipe"])