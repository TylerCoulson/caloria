from fastapi import APIRouter, Depends, status
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from datetime import date
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
async def create_daily(*, deps:LoggedInDeps, date:date = date.today()):
    actual_weight = await api_daily.get_weight(profile_id=deps['profile'].id, current_date=date, db=deps['db']) 
    context = {
                "request": deps['request'],
                "hx_request": deps['hx_request'],
                "user": deps['profile'],
                "date": date,
                "actual_weight": actual_weight.actual_weight if actual_weight else  0
            }
    return templates.TemplateResponse("daily/create_actual_weight.html", context)

@router.get(
    "",
    response_class=HTMLResponse,
    status_code=status.HTTP_200_OK,
)
async def get_all_daily(*, deps:LoggedInDeps, n:int=25, page:int=1, home:bool=False, appending:bool=False):
    
    output_data = await api_daily.get_all_daily(deps=deps, n=n, page=page)
    context = {
                "request": deps['request'],
                "hx_request": deps['hx_request'],
                "user": deps['profile'],
                "dailies": output_data,
                "page": page,
                "home": home,
                "appending": appending
            }
    if appending:
        return templates.TemplateResponse("daily/body.html", context)
    
    return templates.TemplateResponse("daily/base.html", context)

@router.get(
    "/{date}",
    response_class=HTMLResponse,
    status_code=status.HTTP_200_OK,
)
async def get_daily(*, deps:LoggedInDeps, date:date = date.today()):
    
    output_data = await api_daily.get_daily(deps=deps, current_date=date)
    logs = await api_food_log.get_food_log_date(deps=deps, n=25, page=1, date=date)
    logs = logs['log']
    context = {
                "request": deps['request'],
                "hx_request": deps['hx_request'],
                "user": deps['profile'],
                "daily": output_data,
                "logs": logs
            }
    return templates.TemplateResponse("daily/day.html", context)
    
@router.put(
    "/{date}",
    response_class=HTMLResponse,
    status_code=status.HTTP_200_OK,
)
async def update_actual_weight(*, deps:LoggedInDeps, date:date, actual_weight:schemas.ActualWeight):
    daily_data = {"profile_id": deps['profile'].id, "date": date, "actual_weight":actual_weight.actual_weight} 
    
    data = await api_daily.update_daily(deps=deps, current_date=date, daily_data=schemas.DailyOverviewInput(**daily_data))
    
    context = {
                "request": deps['request'],
                "hx_request": deps['hx_request'],
                "user": deps['profile'],
                "daily": data
            }
    return templates.TemplateResponse("daily/weight_column.html", context)

