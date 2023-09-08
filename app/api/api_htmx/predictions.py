from fastapi import APIRouter, Depends, status,Request, Header
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session  # type: ignore
from fastapi.templating import Jinja2Templates

from app import deps
from app.api.api_V1 import predictions
from app.api.api_V1.predictions import weight_params
from app.api.api_htmx.deps import CommonDeps

router = APIRouter(prefix="/prediction")
templates = Jinja2Templates("app/templates")


@router.get(
    "",
    response_class=HTMLResponse,
    status_code=status.HTTP_200_OK,
)
def get_predictions_page(*, common:CommonDeps):
    """ returns page that allows foods searching for food"""

    context = {
            "request": common['request'],
            "hx_request": common['hx_request']
        }
    return templates.TemplateResponse("prediction/base.html", context)


@router.get(
    "/never_faulter",
    response_class=HTMLResponse,
    status_code=status.HTTP_200_OK,
)
async def get_predictions_never_faulter(*, params: dict=Depends(weight_params), common:CommonDeps):
    """ returns page for predictions that never faultered on calories lost """
    pred = await predictions.get_predictions_never_fault(params=params, db=common['db'])
    context = {
            "request": common['request'],
            "hx_request": common['hx_request'],
            "preds": pred,
            "final_day": pred[str(len(pred)-1)]
        }
    return templates.TemplateResponse("prediction/list.html", context)