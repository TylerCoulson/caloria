from fastapi import APIRouter, Depends, status,Request, HTTPException, Header
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session  # type: ignore
from fastapi.templating import Jinja2Templates
from fastapi.encoders import jsonable_encoder

from app import deps
from app import schemas
from app import models
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
def get_create_food(*, request: Request, hx_request: str | None = Header(default=None)):    
    context = {
            "request": request,
            "hx_request": hx_request,
        }

    return templates.TemplateResponse("food/create.html", context)

@router.get(
    "/{food_id:int}",
    response_class=HTMLResponse,
    status_code=status.HTTP_200_OK,
)
async def get_food(*, request: Request, hx_request: str | None = Header(default=None), food_id:int, db: Session = Depends(deps.get_db)):    
    food = await api_food.get_food_id(food_id=food_id, db=db)
    servings = await api_servings.get_serving_size_by_food(food_id=food_id, db=db)
    context = {
            "request": request,
            "hx_request": hx_request,
            "food": food,
            "servings": servings['servings']
        }
    return templates.TemplateResponse("food/item.html", context)


@router.get(
    "/all",
    response_class=HTMLResponse,
    status_code=status.HTTP_200_OK,
)
async def get_all_foods(*, request: Request, hx_request: str | None = Header(default=None), n:int=25, page:int=1, db: Session = Depends(deps.get_db)):
    """ returns page that all foods"""
    data = await api_food.get_all_foods(n=n, page=page, db=db)
    context = {
            "request": request,
            "hx_request": hx_request,
            "foods": data,
        }
    return templates.TemplateResponse("food/list.html", context)

@router.get(
"/search",
response_class=HTMLResponse,
status_code=status.HTTP_200_OK,
)
async def get_search_food_results(*, request: Request,hx_request: str | None = Header(default=None), n:int=25, page:int=1, search_word:str, db: Session = Depends(deps.get_db)):
    """Returns the results of searching for food"""
    data = await api_food.get_food_search(search_word=search_word, n=n, page=page, db=db)

    context = {
        "request": request,
        "hx_request": hx_request,
        "foods": data,
        }

    return templates.TemplateResponse("food/body.html", context)
