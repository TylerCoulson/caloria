from fastapi import APIRouter, Depends, status,Request, HTTPException, Header
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from app import schemas
from app.api.api_htmx.deps import CommonDeps, LoggedInDeps
from app.api.api_V1 import serving_size as api_servings
from app.api.api_htmx.food import router as food_router
from app.api.api_V1 import food as api_food

router = APIRouter()
templates = Jinja2Templates("app/templates")

@router.get(
    "/servings/create/{food_id}",
    response_class=HTMLResponse,
    status_code=status.HTTP_200_OK,
)
async def get_create_serving(*, deps:CommonDeps, food_id:int):

    food = await api_food.get_food_by_id(deps=deps, food_id=food_id)

    context = {
            "request": deps['request'],
            "hx_request": deps['hx_request'],
            "user": deps['user'],
            "food": food
        }
    return templates.TemplateResponse("food/servings/create.html", context)

@router.get(
    "/servings/{serving_id:int}/edit",
    response_class=HTMLResponse,
    status_code=status.HTTP_200_OK,
)
async def get_edit_serving(*, deps:CommonDeps, serving_id:int):

    serving = await api_servings.get_serving_size_by_id(deps=deps, serving_id=serving_id)

    context = {
            "request": deps['request'],
            "hx_request": deps['hx_request'],
            "user": deps['user'],
            "food": serving.food,
            "serving": serving,
            "edit": True
        }
    return templates.TemplateResponse("food/servings/create.html", context)

@router.put(
    "/servings/{serving_id:int}",
    response_class=HTMLResponse,
    status_code=status.HTTP_200_OK,
)
async def update_food(*, deps:LoggedInDeps, serving_id: int, serving_in: schemas.ServingSizeBase):
    update_serving = await api_servings.update_serving_size(deps=deps, food_id=serving_in.food_id, serving_id=serving_id, serving_size_in=serving_in)
    
    servings = await api_servings.get_serving_size_by_food(deps=deps, food_id=update_serving.food_id)
    context = {
        "request": deps['request'],
        "hx_request": deps['hx_request'],
        "user": deps['user'],
        "food": update_serving.food,
        "servings": servings['servings']
    }

    return templates.TemplateResponse("food/servings/base.html", context)

@router.post(
    "/servings",
    response_class=HTMLResponse,
    status_code=status.HTTP_201_CREATED,
)
async def post_servings(*, deps:LoggedInDeps, serving_size: schemas.ServingSizeCreate):
    servings_out = await api_servings.post_serving_size(deps=deps, food_id=serving_size.food_id, serving_size=serving_size)
    food = await api_food.get_food_by_id(deps=deps, food_id=serving_size.food_id)
    context = {
            "request": deps['request'],
            "hx_request": deps['hx_request'],
            "trigger": "click",
            "user": deps['user'],
            "food": food,
            "servings": [servings_out]
        }

    return templates.TemplateResponse("food/servings/base.html", context)



food_router.include_router(router, tags=['htmx-servings'])
