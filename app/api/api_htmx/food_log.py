from fastapi import APIRouter, Depends, status, Request, HTTPException, Header
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session  # type: ignore
from app import deps
from app import schemas
from app import models
from datetime import date
from app.api.api_V1 import food_log as api_food_log
from app import crud
from app.auth.router import Annotated_Profile

router = APIRouter(prefix="/food_log")
templates = Jinja2Templates("app/templates")


@router.get(
    "/all",
    response_class=HTMLResponse,
    status_code=status.HTTP_200_OK,
)
async def get_food_logs(*, request: Request, hx_request: str | None = Header(default=None), n:int=25, page:int=1, db: Session = Depends(deps.get_db)):
    profile = await crud.read(_id=1, db=db, model=models.Profile)
    logs = await api_food_log.get_food_logs(n=n, page=page, profile=profile, db=db)
    
    context = {
            "request": request,
            "hx_request": hx_request,
            "logs": logs,
        }

    return templates.TemplateResponse("log/list.html", context)             

@router.get(
    "/{date}",
    response_class=HTMLResponse,
    status_code=status.HTTP_200_OK,
)
async def get_food_logs_by_profile_date(*, request: Request, hx_request: str | None = Header(default=None), n:int=25, page:int=1, date: date, db: Session = Depends(deps.get_db)):

        profile = await crud.read(_id=1, db=db, model=models.Profile)
        logs = await api_food_log.get_food_log_date(n=n, page=page, date=date, profile=profile, db=db)
        logs = logs['log']
        context = {
                "request": request,
                "hx_request": hx_request,
                "logs": logs,
                "trigger": 'click'
            }
        
        return templates.TemplateResponse("log/day.html", context)

# @router.get(
#     "/create",
#     response_class=HTMLResponse,
#     status_code=status.HTTP_200_OK,
# )
# async def get_create_log(*, request: Request, hx_request: str | None = Header(default=None), db: Session = Depends(deps.get_db), profile: Annotated_Profile,):
#     food = schemas.FoodNoIngredients(brand="", name="", id=0)
#     serving_size = schemas.ServingSize(food_id=0, description="", calories=0, fats=0, carbs=0, protein=0, id=0, food=food)
#     log = schemas.FoodLog(date=date.today(), food_id=0, serving_size_id=0, serving_amount=0, profile_id=profile.id, id=0, serving_size=serving_size)

#     context = {
#             "request": request,
#             "hx_request": hx_request,
#             "trigger": 'click',
#             "log": log
#         }

#     return templates.TemplateResponse("food_log/edit/row_base.html", context)

# @router.get(
#     "/edit/{log_id}",
#     response_class=HTMLResponse,
#     status_code=status.HTTP_200_OK,
# )
# async def get_log_edit(*, request: Request, hx_request: str | None = Header(default=None), profile: Annotated_Profile, log_id:int, copy:bool = False, db: Session = Depends(deps.get_db)):

#     log = await api_food_log.get_food_log_id(profile=profile, food_log_id=log_id, db=db)

#     context = {
#         "request": request,
#         "hx_request": hx_request,
#         "trigger": 'click',
#         "log":log,
#         "editable": True
#     }

#     if copy:
#         context["log"].date = date.today()
#         context["log"].id = 0
#         context['editable'] = False

#     return templates.TemplateResponse("food_log/edit/row_base.html", context)     

# @router.put(
#     "/{food_log_id}",
#     response_class=HTMLResponse,
#     status_code=status.HTTP_201_CREATED,
# )
# async def update_food_log(*, request: Request, hx_request: str | None = Header(default=None), food_log_id: int, food_log_in: schemas.FoodLogBase, profile: Annotated_Profile, db: Session = Depends(deps.get_db)):
    
#     if food_log_id == 0:
#         return post_food_log(request=request, hx_request=hx_request, profile=profile, food_log=food_log_in, db=db)

    
#     log = await api_food_log.update_food_log(food_log_id=food_log_id, food_log_in=food_log_in, profile=profile, db=db)

#     context = {
#             "request": request,
#             "hx_request": hx_request,
#             "logs": [log],
#         }
#     return templates.TemplateResponse("food_log/food_log_body.html", context)

# @router.post(
#     "",
#     response_class=HTMLResponse,
#     status_code=status.HTTP_201_CREATED,
# )
# async def post_food_log(*, request: Request, hx_request: str | None = Header(default=None), profile: Annotated_Profile, food_log: schemas.FoodLogCreate, db: Session = Depends(deps.get_db)):
#     await api_food_log.post_food_log(profile=profile, food_log=food_log, db=db)
#     logs = await api_food_log.get_food_logs(profile=profile, db=db)
#     context = {
#             "request": request,
#             "hx_request": hx_request,
#             "logs": logs,
#         }
#     return templates.TemplateResponse("food_log/food_log.html", context)



# @router.get(
#     "/{food_log_id:int}",
#     response_class=HTMLResponse,
#     status_code=status.HTTP_200_OK,
# )
# async def get_food_log_id(*, request: Request, hx_request: str | None = Header(default=None), profile: Annotated_Profile, food_log_id: int, db: Session = Depends(deps.get_db)):
    
    
#     try:
#         log = await api_food_log.get_food_log_id(profile=profile, food_log_id=food_log_id, db=db)
#         context = {
#                 "request": request,
#                 "hx_request": hx_request,
#                 "logs": [log],
#                 "trigger": None
#             }
#         return templates.TemplateResponse("food_log/food_log_body.html", context)

#     except HTTPException:
#         context = {
#             "request": request,
#             "hx_request": hx_request,
#             "message": f"No log with id of {food_log_id} for {profile.user_id}"
#         }
#         return templates.TemplateResponse("404.html", context)


# @router.delete(
#     "/{food_log_id}",
#     status_code=status.HTTP_200_OK,
# )
# async def delete_food_log(*, request: Request, hx_request: str | None = Header(default=None), food_log_id: int, profile:Annotated_Profile, db: Session = Depends(deps.get_db)):
#     log = await api_food_log.get_food_log_id(profile=profile, food_log_id=food_log_id, db=db)
    
#     await crud.delete(_id=food_log_id, db=db, db_obj=log)
    
#     logs = await api_food_log.get_food_logs(profile=profile, db=db)
#     context = {
#             "request": request,
#             "hx_request": hx_request,
#             "logs": logs,
#             "trigger": 'click'
#         }
#     return templates.TemplateResponse("food_log/food_log.html", context)
