from fastapi import APIRouter, Depends, status, HTTPException, Request, Header
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session  # type: ignore
from fastapi.templating import Jinja2Templates
from fastapi.encoders import jsonable_encoder
from app import deps
from app import models
from app import schemas
from app import crud


router = APIRouter()
templates = Jinja2Templates("app/templates")

tabs = {"home":'active'}
@router.get(
    "/",
    response_class=HTMLResponse,
    status_code=status.HTTP_200_OK,
)
def get_index(request: Request, hx_request: str | None = Header(default=None)):
    context = {
        "request": request,
        "hx_request":hx_request,
        "tabs": tabs
    }

    return templates.TemplateResponse("index.html", context)

@router.get(
    "/navbar",
    response_class=HTMLResponse,
    status_code=status.HTTP_200_OK,
)
def get_index(request: Request, hx_request: str | None = Header(default=None)):
    context = {
        "request": request,
        "hx_request":hx_request,
        "tabs": tabs
    }

    return templates.TemplateResponse("nav.html", context)

# @router.get(
#     "/user",
#     response_class=HTMLResponse,
#     status_code=status.HTTP_200_OK,
# )
# def get_user(*, request: Request,hx_request: str | None = Header(default=None), user_id:int, db: Session = Depends(deps.get_db)):
#     data = db.query(models.User).filter(models.User.id == user_id).first()
#     if data:
#         context = {
#             "request": request,
# "hx_request": hx_request,
#             "user": jsonable_encoder(data)
#         }
#         return templates.TemplateResponse("user.html", context)

#     context = {"request": request}

#     return templates.TemplateResponse("404.html", context)



# @router.post(
#     "/user",
#     response_class=HTMLResponse,
#     status_code=status.HTTP_201_CREATED,
# )
# def post_user(*, request: Request,hx_request: str | None = Header(default=None), User: schemas.UserCreate, db: Session = Depends(deps.get_db)):
#     user_data = crud.create(obj_in=User, db=db, model=models.User)
#     context = {
#             "request": request,
# "hx_request": hx_request,
#             "user": jsonable_encoder(user_data)
#         }
#     return templates.TemplateResponse("user.html", context)


# @router.post(
#     "/food",
#     response_class=HTMLResponse,
#     status_code=status.HTTP_201_CREATED,
# )
# def post_food(*, request: Request,hx_request: str | None = Header(default=None), food: schemas.FoodCreate, db: Session = Depends(deps.get_db)):
#     food_out = crud.create(obj_in=food, db=db, model=models.Food)
#     context = {
#             "request": request,
# "hx_request": hx_request,
#             "foods": [jsonable_encoder(food_out)]
#         }
#     return templates.TemplateResponse("food.html", context)

# @router.get(
#     "/foods",
#     response_class=HTMLResponse,
#     status_code=status.HTTP_201_CREATED,
# )
# def get_search_food(*, request: Request,hx_request: str | None = Header(default=None), db: Session = Depends(deps.get_db)):
#     context = {
#             "request": request,
# "hx_request": hx_request,
#         }
#     return templates.TemplateResponse("food_search.html", context)


# @router.get(
# "/food",
# response_class=HTMLResponse,
# status_code=status.HTTP_201_CREATED,
# )
# def get_foods_brand(*, request: Request,hx_request: str | None = Header(default=None), search_for:str, search_word:str, db: Session = Depends(deps.get_db)):
    
#     data = db.query(models.Food).filter(getattr(models.Food, search_for).contains(search_word)).all()
    
#     headers = jsonable_encoder(data[0]).keys()
#     context = {
#             "request": request,
# "hx_request": hx_request,
#             "foods": jsonable_encoder(data),
#             "headers": headers
#         }
#     return templates.TemplateResponse("food.html", context)