
from fastapi import APIRouter, Depends, status, Request, Header
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from app import deps
from app.auth.db import get_user_db
from app import schemas

router = APIRouter()
templates = Jinja2Templates("app/templates")

@router.get(
    "/register",
    response_class=HTMLResponse,
    status_code=status.HTTP_200_OK,
)
def register(*, request: Request, hx_request: str | None = Header(default=None)):
    context = {
            "request": request,
            "hx_request": hx_request,
        }

    return templates.TemplateResponse("auth/registration/base.html", context)

@router.get(
    "/login",
    response_class=HTMLResponse,
    status_code=status.HTTP_200_OK,
)
def login(*, request: Request, hx_request: str | None = Header(default=None)):
    context = {
            "request": request,
            "hx_request": hx_request,
        }

    return templates.TemplateResponse("auth/login/base.html", context)