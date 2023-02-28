from fastapi import APIRouter, Depends, status,Request, Header
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session  # type: ignore
from fastapi.templating import Jinja2Templates

from datetime import date
from app import deps
from app.api.api_V1 import predictions


router = APIRouter()
templates = Jinja2Templates("app/templates")

tabs = {'prediction': 'active'}
'''
hx_request - Checks if request was made through an hx_request
tabs - which tab should be active in the navigation tab
'''

@router.get(
        "/1",
    response_class=HTMLResponse,
    status_code=status.HTTP_200_OK,
)
def get_predictions_never_faulter(*, user_id:int, request: Request,hx_request: str | None = Header(default=None), db: Session = Depends(deps.get_db)):
    """ returns page that allows foods searching for food"""
    pred = predictions.get_predictions_never_fault(user_id=user_id, db=db)

    context = {
            "request": request,
            "hx_request": hx_request,
            "preds": pred,
            "tabs": tabs
        }
    return templates.TemplateResponse("predictions.html", context)

@router.get(
        "/2",
    response_class=HTMLResponse,
    status_code=status.HTTP_200_OK,
)
def get_predictions_updates(*, user_id:int, current_date:date, request: Request,hx_request: str | None = Header(default=None), db: Session = Depends(deps.get_db)):
    """ returns page that allows foods searching for food"""
    pred = predictions.get_predictions_updates_lbs_to_lose(user_id=user_id, current_date=current_date, db=db)

    context = {
            "request": request,
            "hx_request": hx_request,
            "preds": pred,
            "tabs": tabs
        }
    return templates.TemplateResponse("predictions.html", context)