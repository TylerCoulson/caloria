from fastapi import APIRouter, status, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from app.api.api_htmx.deps import CommonDeps
from pydantic import EmailStr

router = APIRouter(prefix='')
templates = Jinja2Templates("app/templates")

@router.get(
    "/auth_type",
    response_class=HTMLResponse,
    status_code=status.HTTP_200_OK,
)
async def auth_type(deps:CommonDeps, remember:bool = False):
    context = {
        "request": deps['request'],
        "hx_request": deps['hx_request'],
        "user": deps['user'],
        "remember": remember
    }
    
    return templates.TemplateResponse("auth/login/auth_type.html", context)