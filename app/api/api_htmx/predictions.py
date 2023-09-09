from fastapi import APIRouter, Depends, status
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from app.api.api_V1 import predictions
from app.api.api_V1.predictions import weight_params
from app.api.api_htmx.deps import CommonDeps
from app.auth.router import Annotated_Profile

router = APIRouter(prefix="/prediction")
templates = Jinja2Templates("app/templates")


@router.get(
    "",
    response_class=HTMLResponse,
    status_code=status.HTTP_200_OK,
)
async def get_predictions_page(*, deps:CommonDeps, profile:Annotated_Profile=False):
    """ returns page that allows foods searching for food"""

    context = {
            "request": deps['request'],
            "hx_request": deps['hx_request'],
            "user": deps['user'],
            "profile": profile if profile else {"start_date":"", "start_weight":"", "goal_weight":"", "sex":"", "birthdate":"", "height":"", "lbs_per_week":"", "activity_level":""}
        }
    return templates.TemplateResponse("prediction/base.html", context)


@router.get(
    "/never_faulter",
    response_class=HTMLResponse,
    status_code=status.HTTP_200_OK,
)
async def get_predictions_never_faulter(*, params: dict=Depends(weight_params), deps:CommonDeps, profile:Annotated_Profile=False):
    """ returns page for predictions that never faultered on calories lost """
    pred = await predictions.get_predictions_never_fault(params=params)
    context = {
            "request": deps['request'],
            "hx_request": deps['hx_request'],
            "user": deps['user'],
            "profile": profile if profile else {"start_date":"", "start_weight":"", "goal_weight":"", "sex":"", "birthdate":"", "height":"", "lbs_per_week":"", "activity_level":""},
            "preds": pred,
            "final_day": pred[str(len(pred)-1)]
        }
    return templates.TemplateResponse("prediction/list.html", context)