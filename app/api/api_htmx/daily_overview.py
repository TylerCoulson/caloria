from fastapi import APIRouter, Depends, status, Request, HTTPException, Header
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session  # type: ignore
from datetime import date
from app import deps
from app import schemas

from app.api.api_V1 import daily_overview as api_daily

router = APIRouter()
templates = Jinja2Templates("app/templates")

from app import crud

tabs = {'daily': 'active'}
@router.post(
    "",
    response_class=HTMLResponse,
    status_code=status.HTTP_201_CREATED,
)
def post_daily(*, request: Request,hx_request: str | None = Header(default=None), actual_weight:schemas.DailyOverviewInput, db: Session = Depends(deps.get_db)):
    output_data = jsonable_encoder(api_daily.post_daily(actual_weight=actual_weight, db=db))
    context = {
                "request": request,
                "hx_request": hx_request,
                "dailies": [output_data],
                "tabs": tabs
            }

    return templates.TemplateResponse("daily.html", context)


@router.get(
    "",
    response_class=HTMLResponse,
    status_code=status.HTTP_200_OK,
)
def get_daily(*, request: Request,hx_request: str | None = Header(default=None), profile_id:int, date:date = date.today(), db: Session = Depends(deps.get_db)):
    output_data = jsonable_encoder(api_daily.get_daily(profile_id=profile_id, current_date=date, db=db))
    
    context = {
                "request": request,
                "hx_request": hx_request,
                "dailies": [output_data],
                "tabs": tabs
            }
    return templates.TemplateResponse("daily.html", context)
    

@router.get(
    "/all",
    response_class=HTMLResponse,
    status_code=status.HTTP_200_OK,
)
def get_all_daily(*, request: Request,hx_request: str | None = Header(default=None), profile_id:int, n_days:int=50, db: Session = Depends(deps.get_db)):
    
    output_data = jsonable_encoder(api_daily.get_all_daily(profile_id=profile_id, n_days=n_days, db=db))
    # 
    # 
    context = {
                "request": request,
                "hx_request": hx_request,
                "dailies": output_data,
                "tabs": tabs
            }
    
    return templates.TemplateResponse("daily.html", context)