from fastapi import APIRouter, Depends, status
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session 
from datetime import date
from app import deps
from app import schemas

from app.api.api_htmx.deps import LoggedInDeps
from app.api.api_V1 import daily_overview as api_daily
from app.api.api_V1 import food_log as api_food_log

router = APIRouter(prefix="/daily")
templates = Jinja2Templates("app/templates")

from app import crud

@router.get(
    "/create/{date}",
    response_class=HTMLResponse,
    status_code=status.HTTP_200_OK,
)
async def get_daily(*, logged_in:LoggedInDeps, date:date = date.today()):
    actual_weight = await api_daily.get_weight(profile_id=logged_in['profile'].id, current_date=date, db=logged_in['db']) 
    context = {
                "request": logged_in['request'],
                "hx_request": logged_in['hx_request'],
                "user": logged_in['profile'],
                "date": date,
                "actual_weight": actual_weight.actual_weight if actual_weight else  0
            }
    return templates.TemplateResponse("daily/create_actual_weight.html", context)

@router.get(
    "",
    response_class=HTMLResponse,
    status_code=status.HTTP_200_OK,
)
async def get_all_daily(*, logged_in:LoggedInDeps, n:int=25, page:int=1):
    
    output_data = await api_daily.get_all_daily(profile=logged_in['profile'], n=n, page=page, db=logged_in['db'])
    context = {
                "request": logged_in['request'],
                "hx_request": logged_in['hx_request'],
                "user": logged_in['profile'],
                "dailies": output_data,
            }
    
    return templates.TemplateResponse("daily/base.html", context)

@router.get(
    "/{date}",
    response_class=HTMLResponse,
    status_code=status.HTTP_200_OK,
)
async def get_daily(*, logged_in:LoggedInDeps, date:date = date.today()):
    
    output_data = await api_daily.get_daily(profile=logged_in['profile'], current_date=date, db=logged_in['db'])
    logs = await api_food_log.get_food_log_date(n=25, page=1, date=date, profile=logged_in['profile'], db=logged_in['db'])
    logs = logs['log']
    context = {
                "request": logged_in['request'],
                "hx_request": logged_in['hx_request'],
                "user": logged_in['profile'],
                "daily": output_data,
                "logs": logs
            }
    return templates.TemplateResponse("daily/day.html", context)
    
@router.put(
    "/{date}",
    response_class=HTMLResponse,
    status_code=status.HTTP_200_OK,
)
async def update_actual_weight(*, logged_in:LoggedInDeps, date:date, actual_weight:schemas.ActualWeight):
    daily_data = {"profile_id": logged_in['profile'].id, "date": date, "actual_weight":actual_weight.actual_weight} 
    
    data = await api_daily.update_daily(profile=logged_in['profile'], current_date=date, daily_data=schemas.DailyOverviewInput(**daily_data), db=logged_in['db'])
    
    context = {
                "request": logged_in['request'],
                "hx_request": logged_in['hx_request'],
                "user": logged_in['profile'],
                "daily": data
            }
    return templates.TemplateResponse("daily/weight_column.html", context)

