from fastapi import APIRouter, Depends, status,Request, HTTPException, Header
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session  # type: ignore
from fastapi.templating import Jinja2Templates
from fastapi.encoders import jsonable_encoder

from app import deps
from app import schemas
from app import models
from app.api.api_V1 import food as api_food

router = APIRouter()
templates = Jinja2Templates("app/templates")

@router.post(
    "",
    response_class=HTMLResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_user(*, request: Request,hx_request: str | None = Header(default=None), user: schemas.UserCreate, db: Session = Depends(deps.get_db)):
    food_out = jsonable_encoder(api_food.create_user(user=user, db=db))
    # food_out = [schemas.FoodBase(**jsonable_encoder(food_db))]

    context = {
            "request": request,
            "hx_request": hx_request,
            "user": [food_out]
        }
    return templates.TemplateResponse("user.html", context)

@router.get(
    "/{user_id}",
    response_class=HTMLResponse,
    status_code=status.HTTP_200_OK,
)
def get_user(*, request: Request,hx_request: str | None = Header(default=None), user_id: int, db: Session = Depends(deps.get_db)):
    user_out = jsonable_encoder(api_food.get_user_id(user=user_id, db=db))
 
    context = {
            "request": request,
            "hx_request": hx_request,
            "user": user_out
        }
    return templates.TemplateResponse("user.html", context)
