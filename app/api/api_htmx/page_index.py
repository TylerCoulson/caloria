from fastapi import APIRouter, status, Request, Header
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from app.api.api_htmx.deps import CommonDeps, LoggedInDeps
from app.api.api_V1 import daily_overview as api_daily
from app.api.api_htmx import utils
from datetime import date, timedelta,datetime


router = APIRouter()
templates = Jinja2Templates("app/templates")

@router.get(
    "/",
    response_class=HTMLResponse,
    status_code=status.HTTP_200_OK,
)
def get_index(deps:CommonDeps):
    context = {
        "request": deps['request'],
        "hx_request": deps['hx_request'],
        "user": deps['user']
    }

    return templates.TemplateResponse("index/index.html", context, headers={'HX-Redirect': '/'})


@router.get(
    "/calorie_progress"
)
async def calorie_progress(deps:LoggedInDeps):
    offsets = await utils.calorie_progress_data(deps=deps)

    context = {
        "request": deps['request'],
        "hx_request": deps['hx_request'],
        "profile": deps['profile'],
        "offsets": offsets
    }
    return templates.TemplateResponse("index/calorie_progress.html", context)

@router.get(
    "/navbar",
    response_class=HTMLResponse,
    status_code=status.HTTP_200_OK,
)
def get_navbar(deps:CommonDeps):
    context = {
        "request": deps['request'],
        "hx_request": deps['hx_request'],
        "user": deps['user']
    }

    return templates.TemplateResponse("nav.html", context)

@router.get(
    "/not_found",
)
def get_not_found(deps:CommonDeps):
    context = {
        "request": deps['request'],
        "hx_request": deps['hx_request'],
        "user": deps['user']
    }

    return templates.TemplateResponse("404.html", context)