from fastapi import APIRouter, Depends, status,Request, HTTPException, Header
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session  # type: ignore
from fastapi.templating import Jinja2Templates

from app import deps
from app import schemas
from app.api.api_htmx.deps import CommonDeps
from app.api.api_V1 import food as api_food
from app.api.api_V1 import serving_size as api_servings

router = APIRouter(prefix="/food")
templates = Jinja2Templates("app/templates")

'''
hx_request - Checks if request was made through an hx_request
tabs - which tab should be active in the navigation tab
'''

@router.get(
    "/create",
    response_class=HTMLResponse,
    status_code=status.HTTP_200_OK,
)
def get_create_food(*, common:CommonDeps):
    context = {
        "request": common['request'],
        "hx_request": common['hx_request'],
        "user": common['profile']
    }

    return templates.TemplateResponse("food/create.html", context)

@router.get(
    "/{food_id:int}",
    response_class=HTMLResponse,
    status_code=status.HTTP_200_OK,
)
async def get_food(*, common:CommonDeps, food_id:int):    
    food = await api_food.get_food_id(food_id=food_id, db=common['db'])
    servings = await api_servings.get_serving_size_by_food(food_id=food_id, db=common['db'])
    context = {
        "request": common['request'],
        "hx_request": common['hx_request'],
        "user": common['profile'],
        "food": food,
        "servings": servings['servings']
    }
    return templates.TemplateResponse("food/item.html", context)


@router.get(
    "/all",
    response_class=HTMLResponse,
    status_code=status.HTTP_200_OK,
)
async def get_all_foods(*, common:CommonDeps, n:int=25, page:int=1):
    """ returns page that all foods"""
    data = await api_food.get_all_foods(n=n, page=page, db=common['db'])
    context = {
        "request": common['request'],
        "hx_request": common['hx_request'],
        "user": common['profile'],
        "foods": data,
    }
    return templates.TemplateResponse("food/list.html", context)

@router.get(
"/search",
response_class=HTMLResponse,
status_code=status.HTTP_200_OK,
)
async def get_search_food_results(*, common:CommonDeps, n:int=25, page:int=1, search_word:str):
    """Returns the results of searching for food"""
    data = await api_food.get_food_search(search_word=search_word, n=n, page=page, db=common['db'])

    context = {
        "request": common['request'],
        "hx_request": common['hx_request'],
        "user": common['profile'],
        "foods": data,
    }

    return templates.TemplateResponse("food/body.html", context)

@router.post(
    "",
    response_class=HTMLResponse,
    status_code=status.HTTP_201_CREATED,
)
async def post_food(*, common:CommonDeps, food: schemas.FoodCreate):
    
    await api_food.post_food(food=food, db=common['db'])
    foods = await api_food.get_all_foods(db=common['db'])
    
    context = {
        "request": common['request'],
        "hx_request": common['hx_request'],
        "user": common['profile'],
        "foods": foods,
    }
    return templates.TemplateResponse("food/list.html", context)     