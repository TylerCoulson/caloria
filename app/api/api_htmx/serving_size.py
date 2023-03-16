from fastapi import APIRouter, Depends, status,Request, HTTPException, Header
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session  # type: ignore
from fastapi.templating import Jinja2Templates
from fastapi.encoders import jsonable_encoder

from app import deps
from app import schemas
from app import models
from app.api.api_V1 import serving_size as api_servings

router = APIRouter()
templates = Jinja2Templates("app/templates")

tabs = {"food", 'active'}
@router.post(
    "",
    response_class=HTMLResponse,
    status_code=status.HTTP_201_CREATED,
)
def post_servings(*, request: Request, hx_request: str | None = Header(default=None), serving_size: schemas.ServingSizeCreate, db: Session = Depends(deps.get_db)):
    servings_out = jsonable_encoder(api_servings.post_serving_size(serving_size=serving_size, db=db))
    # servings_out = [schemas.FoodBase(**jsonable_encoder(food_db))]

    context = {
            "request": request,
            "hx_request": hx_request,
            "trigger": "click",
            "servings": [servings_out]
        }

    return templates.TemplateResponse("servings.html", context)

@router.get(
    "/{serving_size_id}",
    response_class=HTMLResponse,
    status_code=status.HTTP_200_OK,
)
def get_serving_size_id(*, request: Request, hx_request: str | None = Header(default=None), serving_size_id: int, db: Session = Depends(deps.get_db)) -> list[schemas.FoodLog]:

    servings_out = jsonable_encoder(api_servings.get_serving_size_id(serving_size_id=serving_size_id, db=db))
    context = {
            "request": request,
            "hx_request": hx_request,
            "trigger": None,
            "servings": [servings_out]
        }
    return templates.TemplateResponse("servings.html", context)

@router.get(
    "/food_id/{food_id}",
    response_class=HTMLResponse,
    status_code=status.HTTP_200_OK,
)
def get_serving_size_by_food(*, request: Request, hx_request: str | None = Header(default=None), food_id: int, db: Session = Depends(deps.get_db)) -> list[schemas.FoodLog]:
    servings_out = jsonable_encoder(api_servings.get_serving_size_by_food(food_id=food_id, db=db))
    context = {
            "request": request,
            "hx_request": hx_request,
            "trigger": "click",
            "servings": servings_out['servings']
        }
    return templates.TemplateResponse("servings.html", context)