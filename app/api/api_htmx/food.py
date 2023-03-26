from fastapi import APIRouter, Depends, status,Request, HTTPException, Header
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session  # type: ignore
from fastapi.templating import Jinja2Templates
from fastapi.encoders import jsonable_encoder

from app import deps
from app import schemas
from app import models
from app.api.api_V1 import food as api_food


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
def get_create_serving_page(*, request: Request, hx_request: str | None = Header(default=None), db: Session = Depends(deps.get_db)):
    
    context = {
            "request": request,
            "hx_request": hx_request,
            "trigger": 'click'
        }

    return templates.TemplateResponse("create_food.html", context)

@router.get(
    "",
    response_class=HTMLResponse,
    status_code=status.HTTP_200_OK,
)
def get_search_page(*, request: Request,hx_request: str | None = Header(default=None), db: Session = Depends(deps.get_db)):
    """ returns page that allows foods searching for food"""
    context = {
            "request": request,
            "hx_request": hx_request,
        }
    return templates.TemplateResponse("food_search.html", context)

@router.post(
    "",
    response_class=HTMLResponse,
    status_code=status.HTTP_201_CREATED,
)
async def post_food(*, request: Request,hx_request: str | None = Header(default=None), food: schemas.FoodCreate, db: Session = Depends(deps.get_db)):
    food_out = await api_food.post_food(food=food, db=db)

    context = {
            "request": request,
            "hx_request": hx_request,
            "foods": [food_out]
        }
    return templates.TemplateResponse("food.html", context)


@router.get(
    "/{food_id:int}",
    response_class=HTMLResponse,
    status_code=status.HTTP_200_OK,
)
async def get_food(*, request: Request,hx_request: str | None = Header(default=None), food_id: int, db: Session = Depends(deps.get_db)):
    food_out = await api_food.get_food_id(food_id=food_id, db=db)
    
    context = {
            "request": request,
            "hx_request": hx_request,
            "trigger": None,
            "include_servings": True,
            "foods": [food_out],
        }
    return templates.TemplateResponse("food.html", context)

@router.get(
"/search",
response_class=HTMLResponse,
status_code=status.HTTP_200_OK,
)
async def get_search_food_results(*, request: Request,hx_request: str | None = Header(default=None), n:int=25, search_word:str, db: Session = Depends(deps.get_db)):
    """Returns the results of searching for food"""
    try:
        data = await api_food.get_food_search(search_word=search_word, n=n, db=db)

        context = {
            "request": request,
            "hx_request": hx_request,
            "foods": data,
            "trigger": "click",
            }

        return templates.TemplateResponse("food.html", context)
    
    except HTTPException:
        context = {
            "request": request,
            "hx_request": hx_request,
            "message": f"No food with {search_word}"
        }
        return templates.TemplateResponse("404.html", context)

@router.get(
    "/all",
    response_class=HTMLResponse,
    status_code=status.HTTP_200_OK,
)
async def get_all_foods(*, request: Request, hx_request: str | None = Header(default=None), n:int=25, db: Session = Depends(deps.get_db)):
    """ returns page that all foods"""
    data = await api_food.get_all_foods(n=n, db=db)
    context = {
            "request": request,
            "hx_request": hx_request,
            "foods": data,
        }
    return templates.TemplateResponse("food.html", context)

@router.get(
    "/all_options",
    response_class=HTMLResponse,
    status_code=status.HTTP_200_OK,
)
async def get_all_foods(*, request: Request, hx_request: str | None = Header(default=None), n:int=25, db: Session = Depends(deps.get_db)):
    """ returns page that all foods"""
    data = await api_food.get_all_foods(n=n, db=db)
    context = {
            "request": request,
            "hx_request": hx_request,
            "foods": data,
        }
    return templates.TemplateResponse("food_log/food_option.html", context)


@router.get(
"/search_options",
response_class=HTMLResponse,
status_code=status.HTTP_200_OK,
)
async def get_search_food_results(*, request: Request,hx_request: str | None = Header(default=None), n:int=25, search_word:str, db: Session = Depends(deps.get_db)):
    """Returns the results of searching for food"""
    data = await api_food.get_food_search(search_word=search_word, n=n, db=db)

    context = {
        "request": request,
        "hx_request": hx_request,
        "foods": data,
        }

    return templates.TemplateResponse("food_log/food_option.html", context)