from fastapi import APIRouter, Depends, status
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from datetime import date
from app import schemas

from app.api.api_htmx.deps import LoggedInDeps
from app.api.api_V1 import daily_overview as api_daily
from app.api.api_htmx import page_index as api_page
from app.api.api_htmx import utils
from app.api.api_V1 import food_log as api_food_log
from app.api.api_V1 import utils

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
    "/create/{date}/activity_level",
    response_class=HTMLResponse,
    status_code=status.HTTP_200_OK,
)
async def create_activity_level(*, deps:LoggedInDeps, date:date = date.today()):
    activity_level = await utils.get_day_activity_level(profile_id=deps['profile'].id, current_date=date, db=deps['db'])

    context = {
                "request": deps['request'],
                "hx_request": deps['hx_request'],
                "user": deps['profile'],
                "date": date,
                "activity_level": activity_level if activity_level else  deps['profile'].activity_level
            }
    return templates.TemplateResponse("daily/create_activity_level.html", context)

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
    progress_circle_data = await utils.calorie_progress_data(deps=deps, overview=output_data)
    logs = logs['log']
    context = {
                "request": deps['request'],
                "hx_request": deps['hx_request'],
                "user": deps['profile'],
                "daily": output_data,
                "logs": logs,
                "offsets": progress_circle_data
            }
    return templates.TemplateResponse("daily/day.html", context)
    
@router.put(
    "/{date}",
    response_class=HTMLResponse,
    status_code=status.HTTP_200_OK,
)
async def update_actual_weight(*, deps:LoggedInDeps, actual_weight:bool=False, activity_level:bool=False, date:date, data:schemas.DailyOptions):
    daily_data = {"profile_id": deps['profile'].id, "date": date, "actual_weight":data.actual_weight, "activity_level":data.activity_level} 

    data = await api_daily.update_daily(deps=deps, current_date=date, daily_data=schemas.DailyOverviewInput(**daily_data), actual_weight=actual_weight, activity_level=activity_level)
    context = {
                "request": deps['request'],
                "hx_request": deps['hx_request'],
                "user": deps['profile'],
                "daily": data
            }

    if actual_weight:
        return templates.TemplateResponse("daily/weight_column.html", context)
    if activity_level:
        return templates.TemplateResponse("daily/activity_level.html", context)
