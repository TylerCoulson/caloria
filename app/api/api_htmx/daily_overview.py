from fastapi import APIRouter, Depends, status, Request, HTTPException, Header
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session  # type: ignore
from datetime import date
from app import deps
from app import schemas
from app import models

from app.api.api_V1 import daily_overview as api_daily
from app.api.api_V1 import food_log as api_food_log
from app.auth.router import Annotated_Profile

router = APIRouter(prefix="/daily")
templates = Jinja2Templates("app/templates")

from app import crud

@router.get(
    "/create/{date}",
    response_class=HTMLResponse,
    status_code=status.HTTP_200_OK,
)
async def get_daily(*, request: Request, hx_request: str | None = Header(default=None), profile: Annotated_Profile, date:date = date.today(), db: Session = Depends(deps.get_db)):
    actual_weight = await api_daily.get_weight(profile_id=profile.id, current_date=date, db=db) 
    context = {
                "request": request,
                "hx_request": hx_request,
                "date": date,
                "actual_weight": actual_weight.actual_weight if actual_weight else  0
            }
    return templates.TemplateResponse("daily/create_actual_weight.html", context)

@router.get(
    "",
    response_class=HTMLResponse,
    status_code=status.HTTP_200_OK,
)
async def get_all_daily(*, request: Request,hx_request: str | None = Header(default=None), profile: Annotated_Profile, n:int=25, page:int=1, db: Session = Depends(deps.get_db)):
    
    output_data = await api_daily.get_all_daily(profile=profile, n=n, page=page, db=db)
    context = {
                "request": request,
                "hx_request": hx_request,
                "dailies": output_data,
            }
    
    return templates.TemplateResponse("daily/base.html", context)

@router.get(
    "/{date}",
    response_class=HTMLResponse,
    status_code=status.HTTP_200_OK,
)
async def get_daily(*, request: Request, hx_request: str | None = Header(default=None), profile: Annotated_Profile, date:date = date.today(), db: Session = Depends(deps.get_db)):
    
    output_data = await api_daily.get_daily(profile=profile,current_date=date, db=db)
    logs = await api_food_log.get_food_log_date(n=25, page=1, date=date, profile=profile, db=db)
    logs = logs['log']
    context = {
                "request": request,
                "hx_request": hx_request,
                "daily": output_data,
                "logs": logs
            }
    return templates.TemplateResponse("daily/day.html", context)
    
@router.put(
    "/{date}",
    response_class=HTMLResponse,
    status_code=status.HTTP_200_OK,
)
async def update_actual_weight(*, request: Request, hx_request: str | None = Header(default=None), profile: Annotated_Profile, date:date, actual_weight:schemas.ActualWeight, db: Session = Depends(deps.get_db)):
    daily_data = {"profile_id": profile.id, "date": date, "actual_weight":actual_weight.actual_weight} 
    data = await api_daily.update_daily(profile=profile, current_date=date, daily_data=schemas.DailyOverviewInput(**daily_data), db=db)
    context = {
                "request": request,
                "hx_request": hx_request,
                "daily": data
            }
    return templates.TemplateResponse("daily/weight_column.html", context)

