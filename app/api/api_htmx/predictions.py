from fastapi import APIRouter, Depends, status,Request, Header
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session  # type: ignore
from fastapi.templating import Jinja2Templates

from datetime import date
from app import deps
from app.api.api_V1 import predictions
from app.api.api_V1.predictions import weight_params

router = APIRouter(prefix="/prediction")
templates = Jinja2Templates("app/templates")


@router.get(
    "",
    response_class=HTMLResponse,
    status_code=status.HTTP_200_OK,
)
def get_predictions_never_faulter(*, request: Request,hx_request: str | None = Header(default=None), db: Session = Depends(deps.get_db)):
    """ returns page that allows foods searching for food"""

    context = {
            "request": request,
            "hx_request": hx_request
        }
    return templates.TemplateResponse("create_prediction.html", context)


@router.get(
    "/never_faulter",
    response_class=HTMLResponse,
    status_code=status.HTTP_200_OK,
)
async def get_predictions_never_faulter(*, params: dict=Depends(weight_params), request: Request,hx_request: str | None = Header(default=None), db: Session = Depends(deps.get_db)):
    """ returns page for predictions that never faultered on calories lost """
    print('\n\ntesting 1\n')
    pred = await predictions.get_predictions_never_fault(params=params, db=db)
    print('\n\ntesting 2\n')
    context = {
            "request": request,
            "hx_request": hx_request,
            "preds": pred
        }
    return templates.TemplateResponse("predictions.html", context)

@router.get(
    "/get_predictions_updates_lbs_to_lose",
    response_class=HTMLResponse,
    status_code=status.HTTP_200_OK,
)
def get_predictions_updates(*, params: dict=Depends(weight_params), current_date:date=None, request: Request,hx_request: str | None = Header(default=None), db: Session = Depends(deps.get_db)):
    """ returns page for predictions that your activity level is updated based on what you actually ate"""
    pred = predictions.get_predictions_updates_lbs_to_lose(params=params, current_date=current_date, db=db)

    context = {
            "request": request,
            "hx_request": hx_request,
            "preds": pred
        }
    return templates.TemplateResponse("predictions.html", context)