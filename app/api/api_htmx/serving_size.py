from fastapi import APIRouter, Depends, status,Request, HTTPException, Header
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from app import deps
from app.api.api_htmx.deps import CommonDeps
from app.api.api_V1 import serving_size as api_servings
from app.api.api_htmx.food import router as food_router
from app.api.api_V1 import food as api_food
from app.auth.router import Annotated_User

router = APIRouter()
templates = Jinja2Templates("app/templates")

@router.get(
    "/servings/create/{food_id}",
    response_class=HTMLResponse,
    status_code=status.HTTP_200_OK,
)
async def get_create_serving(*, deps:CommonDeps, food_id:int):

    food = await api_food.get_food_id(deps=deps, food_id=food_id)

    context = {
            "request": deps['request'],
            "hx_request": deps['hx_request'],
            "user": deps['user'],
            "food": food
        }
    return templates.TemplateResponse("food/servings/create.html", context)

# @router.post(
#     "/servings",
#     response_class=HTMLResponse,
#     status_code=status.HTTP_201_CREATED,
# )
# async def post_servings(*, request: Request, hx_request: str | None = Header(default=None), serving_size: schemas.ServingSizeCreate, db: Session = Depends(deps.get_db)):
#     servings_out = await api_servings.post_serving_size(serving_size=serving_size, db=db)

#     context = {
#             "request": request,
#             "hx_request": hx_request,
#             "trigger": "click",
#             "servings": [servings_out]
#         }

#     return templates.TemplateResponse("servings.html", context)

# @router.get(
#     "/{food_id:int}/serving/{serving_id:int}",
#     response_class=HTMLResponse,
#     status_code=status.HTTP_200_OK,
# )
# async def get_serving_size_id(*, request: Request, hx_request: str | None = Header(default=None), serving_id: int, db: Session = Depends(deps.get_db)) -> list[schemas.FoodLog]:

#     servings_out = await api_servings.get_serving_size_id(serving_id=serving_id, db=db)
#     context = {
#             "request": request,
#             "hx_request": hx_request,
#             "trigger": None,
#             "servings": [servings_out]
#         }
#     return templates.TemplateResponse("servings.html", context)

# @router.get(
#     "/{food_id:int}/servings",
#     response_class=HTMLResponse,
#     status_code=status.HTTP_200_OK,
# )
# async def get_all_servings_for_a_food(*, request: Request, hx_request: str | None = Header(default=None), food_id: int, db: Session = Depends(deps.get_db)) -> list[schemas.FoodLog]:
#     servings_out = await api_servings.get_serving_size_by_food(food_id=food_id, db=db)
#     context = {
#             "request": request,
#             "hx_request": hx_request,
#             "trigger": "click",
#             "servings": servings_out['servings']
#         }
#     return templates.TemplateResponse("servings.html", context)


# @router.get(
#     "/servings",
#     response_class=HTMLResponse,
#     status_code=status.HTTP_200_OK,
# )
# async def get_all_servings_for_a_food(*, request: Request, hx_request: str | None = Header(default=None), food_id: int, db: Session = Depends(deps.get_db)) -> list[schemas.FoodLog]:
#     servings_out = await api_servings.get_serving_size_by_food(food_id=food_id, db=db)
#     context = {
#             "request": request,
#             "hx_request": hx_request,
#             "trigger": "click",
#             "servings": servings_out['servings']
#         }
#     return templates.TemplateResponse("food_log/serving_option.html", context)


food_router.include_router(router, tags=['htmx-servings'])
