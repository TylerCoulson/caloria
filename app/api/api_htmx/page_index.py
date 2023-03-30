from fastapi import APIRouter, status, Request, Header
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from app.auth.router import Annotated_User

router = APIRouter()
templates = Jinja2Templates("app/templates")

@router.get(
    "/",
    response_class=HTMLResponse,
    status_code=status.HTTP_200_OK,
)
def get_index(request: Request, profile: Annotated_User, hx_request: str | None = Header(default=None)):
    context = {
        "request": request,
        "hx_request":hx_request,
        "user": profile
    }

    return templates.TemplateResponse("index.html", context, headers={'HX-Refresh': 'true'})

@router.get(
    "/navbar",
    response_class=HTMLResponse,
    status_code=status.HTTP_200_OK,
)
def get_navbar(request: Request, hx_request: str | None = Header(default=None)):
    
    context = {
        "request": request,
        "hx_request":hx_request,
    }

    return templates.TemplateResponse("nav.html", context)