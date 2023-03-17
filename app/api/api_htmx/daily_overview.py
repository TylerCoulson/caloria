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
from app.auth.router import get_current_profile

router = APIRouter(prefix="/daily")
templates = Jinja2Templates("app/templates")

from app import crud

@router.get(
    "/create",
    response_class=HTMLResponse,
    status_code=status.HTTP_200_OK,
)
def get_create_daily(*, request: Request, hx_request: str | None = Header(default=None), db: Session = Depends(deps.get_db)):
    # output_data = jsonable_encoder(api_daily.get_daily(profile_id=profile_id, date=date, db=db))
    context = {
            "request": request,
            "hx_request": hx_request,
            "trigger": 'click'
        }

    return templates.TemplateResponse("create_actual_weight.html", context)


@router.post(
    "",
    response_class=HTMLResponse,
    status_code=status.HTTP_201_CREATED,
)
async def post_daily(*, request: Request,hx_request: str | None = Header(default=None), actual_weight:schemas.DailyOverviewInput, profile: models.Profile = Depends(get_current_profile), db: Session = Depends(deps.get_db)):
    output_data = await api_daily.post_daily(actual_weight=actual_weight, profile=profile, db=db)
    context = {
                "request": request,
                "hx_request": hx_request,
                "dailies": [output_data],
            }

    return templates.TemplateResponse("daily.html", context)

@router.get(
    "",
    response_class=HTMLResponse,
    status_code=status.HTTP_200_OK,
)
async def get_all_daily(*, request: Request,hx_request: str | None = Header(default=None), profile: models.Profile = Depends(get_current_profile), n_days:int=50, db: Session = Depends(deps.get_db)):

    output_data = await api_daily.get_all_daily(profile=profile, n_days=n_days, db=db)
    context = {
                "request": request,
                "hx_request": hx_request,
                "dailies": output_data,
            }
    
    return templates.TemplateResponse("daily.html", context)

@router.get(
    "/{date}",
    response_class=HTMLResponse,
    status_code=status.HTTP_200_OK,
)
async def get_daily(*, request: Request, hx_request: str | None = Header(default=None), profile: models.Profile = Depends(get_current_profile),  date:date = date.today(), db: Session = Depends(deps.get_db)):
    output_data = await api_daily.get_daily(profile=profile,current_date=date, db=db)
    
    context = {
                "request": request,
                "hx_request": hx_request,
                "dailies": [output_data],
            }
    return templates.TemplateResponse("daily.html", context)
    

