from fastapi import APIRouter, status, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from app.api.api_htmx.deps import CommonDeps
from pydantic import EmailStr

router = APIRouter(prefix='')
templates = Jinja2Templates("app/templates")

@router.get(
    "/reset-password",
    response_class=HTMLResponse,
    status_code=status.HTTP_200_OK,
)
async def reset_password(deps:CommonDeps, token:str = None):
    context = {
        "request": deps['request'],
        "hx_request": deps['hx_request'],
        "user": deps['user'],
        "token": token
    }
    
    return templates.TemplateResponse("auth/reset_password.html", context)

@router.get(
    "/forgot-password",
    response_class=HTMLResponse,
    status_code=status.HTTP_200_OK,
)
async def reset_password(deps:CommonDeps, token:str = None):
    context = {
        "request": deps['request'],
        "hx_request": deps['hx_request'],
        "user": deps['user'],
    }
    
    return templates.TemplateResponse("auth/forgot_password.html", context)