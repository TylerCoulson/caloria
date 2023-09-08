from fastapi import APIRouter, status, Request, Header
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from app.api.api_htmx.deps import CommonDeps


router = APIRouter()
templates = Jinja2Templates("app/templates")

@router.get(
    "/",
    response_class=HTMLResponse,
    status_code=status.HTTP_200_OK,
)
def get_index(common:CommonDeps):
    context = {
        "request": common['request'],
        "hx_request": common['hx_request'],
        "user": common['profile']
    }

    return templates.TemplateResponse("index/index.html", context, headers={'HX-Redirect': '/'})

@router.get(
    "/navbar",
    response_class=HTMLResponse,
    status_code=status.HTTP_200_OK,
)
def get_navbar(common:CommonDeps):
    context = {
        "request": common['request'],
        "hx_request": common['hx_request'],
        "user": common['profile']
    }

    return templates.TemplateResponse("nav.html", context)