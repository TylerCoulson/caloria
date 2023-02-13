from fastapi import APIRouter, Depends, status, Request, HTTPException, Header
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session  # type: ignore
from app import deps
from app import schemas
from app import models
from datetime import date
from app.api.api_V1 import food_log as api_food_log
from app import crud

router = APIRouter()
templates = Jinja2Templates("app/templates")


tabs = {'food_log': 'active'}
@router.post(
    "",
    response_class=HTMLResponse,
    status_code=status.HTTP_201_CREATED,
)
def post_food_log(*, request: Request, hx_request: str | None = Header(default=None), food_log: schemas.FoodLogCreate, db: Session = Depends(deps.get_db)):
    log = jsonable_encoder(api_food_log.post_food_log(food_log=food_log, db=db))
    print("post", log)
    context = {
            "request": request,
            "hx_request": hx_request,
            "logs": [log],
            "tabs": tabs
        }
    return templates.TemplateResponse("food_log.html", context)

@router.get(
    "",
    response_class=HTMLResponse,
    status_code=status.HTTP_200_OK,
)
def get_food_logs(*, request: Request, hx_request: str | None = Header(default=None), user_id:int, db: Session = Depends(deps.get_db)):
    print("testing")
    try:
        logs = jsonable_encoder(api_food_log.get_food_logs(user_id=user_id, db=db))
        context = {
                "request": request,
                "hx_request": hx_request,
                "logs": logs,
                "tabs": tabs,
                "trigger": 'click'
            }

        return templates.TemplateResponse("food_log.html", context)
    
    except HTTPException:
        context = {
            "request": request,
            "hx_request": hx_request,
            "message": f"No logs"
        }
        return templates.TemplateResponse("404.html", context)
        
@router.get(
    "/dates",
    response_class=HTMLResponse,
    status_code=status.HTTP_200_OK,
)
def get_food_logs_by_user_date(*, request: Request, hx_request: str | None = Header(default=None), date: date, user_id:int, db: Session = Depends(deps.get_db)):

    try:
        logs = jsonable_encoder(api_food_log.get_food_log_date(date=date, user_id=user_id, db=db))['log']
        context = {
                "request": request,
                "hx_request": hx_request,
                "logs": logs,
                "tabs": tabs,
                "trigger": 'click'
            }

        return templates.TemplateResponse("food_log.html", context)
    
    except HTTPException:
        context = {
            "request": request,
            "hx_request": hx_request,
            "message": f"No logs for {date} by {user_id}"
        }
        return templates.TemplateResponse("404.html", context)
        
@router.get(
    "/{food_log_id}",
    response_class=HTMLResponse,
    status_code=status.HTTP_200_OK,
)
def get_food_log_id(*, request: Request, hx_request: str | None = Header(default=None), food_log_id: int, db: Session = Depends(deps.get_db)):
    log = jsonable_encoder(api_food_log.get_food_log_id(food_log_id=food_log_id, db=db))
    print(log)    
    context = {
            "request": request,
            "hx_request": hx_request,
            "logs": [log],
            "tabs": tabs,
            "trigger": None
        }
    return templates.TemplateResponse("food_log.html", context)



    

'''CREATE A ROUTE TO GET ALL USER FOOD LOGS. Be able to copy/add prior logs to the different days'''
# @router.put(
#     "/{food_log_id}",
#     response_class=HTMLResponse,
#     status_code=status.HTTP_200_OK,
# )
# def update_food_log(
#     *, request: Request, hx_request: str | None = Header(default=None), food_log_id: int, food_log_in: schemas.FoodLogBase, db: Session = Depends(deps.get_db)
# ):
#     data = get_food_log(food_log_id=food_log_id, db=db)

#     data = crud.update(db_obj=data, data_in=food_log_in, db=db)
#     return data


# @router.delete(
#     "/{food_log_id}",
#     status_code=status.HTTP_200_OK,
# )
# def delete_food_log(*, request: Request, hx_request: str | None = Header(default=None), food_log_id: int, db: Session = Depends(deps.get_db)):
#     data = get_food_log(food_log_id=food_log_id, db=db)

#     data = crud.delete(_id=food_log_id, db=db, db_obj=data)
#     return data
