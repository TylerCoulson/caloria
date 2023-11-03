from fastapi import APIRouter, status
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

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
def get_create_food(*, deps:CommonDeps):
    context = {
        "request": deps['request'],
        "hx_request": deps['hx_request'],
        "user": deps['user']
    }

    return templates.TemplateResponse("food/create.html", context)

@router.get(
    "/{food_id:int}",
    response_class=HTMLResponse,
    status_code=status.HTTP_200_OK,
)
async def get_food(*, deps:CommonDeps, food_id:int):    
    food = await api_food.get_food_id(food_id=food_id, deps=deps)
    servings = await api_servings.get_serving_size_by_food(food_id=food_id, deps=deps)
    context = {
        "request": deps['request'],
        "hx_request": deps['hx_request'],
        "user": deps['user'],
        "food": food,
        "servings": servings['servings']
    }
    return templates.TemplateResponse("food/servings.html", context)


@router.get(
    "/all",
    response_class=HTMLResponse,
    status_code=status.HTTP_200_OK,
)
async def get_all_foods(*, deps:CommonDeps, n:int=25, page:int=1, appending:bool=False):
    """ returns page that all foods"""
    data = await api_food.get_food_types(deps=deps, n=n, page=page)
    context = {
        "request": deps['request'],
        "hx_request": deps['hx_request'],
        "user": deps['user'],
        "foods": data,
        "page": page,
        "appending": appending
    }
    if appending:
        return templates.TemplateResponse("food/body.html", context)
    
    return templates.TemplateResponse("food/list.html", context)

@router.get(
    "/{type:str}/subtypes",
    response_class=HTMLResponse,
    status_code=status.HTTP_200_OK,
)
async def get_subtypes(*, deps:CommonDeps, n:int=25, page:int=1, appending:bool=False, type:str):
    """ returns page that all foods"""
    data = await api_food.get_food_subtypes(deps=deps, n=n, page=page, type=type.lower())
    context = {
        "request": deps['request'],
        "hx_request": deps['hx_request'],
        "user": deps['user'],
        "subtypes": data,
        "page": page,
        "appending": appending
    }
    if appending:
        return templates.TemplateResponse("food/body.html", context)
    
    return templates.TemplateResponse("food/subtype.html", context)

@router.get(
"/search",
response_class=HTMLResponse,
status_code=status.HTTP_200_OK,
)
async def get_search_food_results(*, deps:CommonDeps, n:int=25, page:int=1, search_word:str):
    """Returns the results of searching for food"""
    data = await api_food.get_food_search(search_word=search_word, n=n, page=page, deps=deps)

    context = {
        "request": deps['request'],
        "hx_request": deps['hx_request'],
        "user": deps['user'],
        "foods": data,
        "page": page,
        "search_word": search_word
    }

    return templates.TemplateResponse("food/body.html", context)

@router.post(
    "",
    response_class=HTMLResponse,
    status_code=status.HTTP_201_CREATED,
)
async def post_food(*, deps:CommonDeps, food: schemas.FoodCreate):
    
    new_food = await api_food.post_food(deps=deps, food=food)
    # foods = await api_food.get_all_foods(deps=deps)
    
    context = {
        "request": deps['request'],
        "hx_request": deps['hx_request'],
        "user": deps['user'],
        "food": new_food,
    }
    return templates.TemplateResponse("food/servings/create.html", context)     