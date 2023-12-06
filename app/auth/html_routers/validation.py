from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi_users import InvalidPasswordException
from app.auth.schemas import UserCreate
from app.auth.db import get_user_db
from app.auth.users import get_user_manager
from pydantic import ValidationError
from app.api.api_htmx.deps import CommonDeps

router = APIRouter(prefix='/validate')
templates = Jinja2Templates("app/templates")

@router.get(
    "/password",
    response_class=HTMLResponse,
    status_code=status.HTTP_200_OK,
)
async def validate_passsword(deps:CommonDeps, email:str, password:str, manager = Depends(get_user_manager)):

    context = {
        "request": deps['request'],
        "hx_request": deps['hx_request'],
        "is_valid": True,
        "password": password or ""
    }

    try:
        await manager.validate_password(email=email, password=password)
    except InvalidPasswordException:
        context['is_valid'] = False

    return templates.TemplateResponse("auth/registration/password.html", context)

@router.get(
    "/password_confirm",
    response_class=HTMLResponse,
    status_code=status.HTTP_200_OK,
)
async def confirm_password(deps:CommonDeps, password:str, password_confirm:str):
    context = {
        "request": deps['request'],
        "hx_request": deps['hx_request'],
        "is_valid": True if password == password_confirm else False,
        "password": password or "",
        "password_confirm": password_confirm or ""
    }

    return templates.TemplateResponse("auth/registration/password-confirm.html", context) 

@router.get(
    "/email",
    response_class=HTMLResponse,
    status_code=status.HTTP_200_OK,
)
async def validate_email(*, deps:CommonDeps, email:str, db = Depends(get_user_db)):
    context = {
        "request": deps['request'],
        "hx_request": deps['hx_request'],
        "is_valid": True,
        "is_unique": True,
        "email": email or ""
    }
    try:
        UserCreate(email=email, password="password")
    except ValidationError:
        context['is_valid'] = False
    
    user = await db.get_by_email(email=email)
    if user:
        context['is_unique'] = False

    return templates.TemplateResponse("auth/registration/email.html", context)

@router.get(
    "/submit",
    response_class=HTMLResponse,
    status_code=status.HTTP_200_OK,
)
async def submit(deps:CommonDeps, password:str, password_confirm:str, email:str, manager = Depends(get_user_manager), db = Depends(get_user_db) ):
    context = {
        "request": deps['request'],
        "hx_request": deps['hx_request'],
        "is_valid": False
    }

    
    confirm_valid = await confirm_password(deps=deps, password=password, password_confirm=password_confirm)
    password_valid = await validate_passsword(deps=deps, email=email, password=password, manager=manager)
    email_valid = await validate_email(deps=deps, email=email, db=db)

    if confirm_valid.context['is_valid'] and password_valid.context['is_valid'] and email_valid.context['is_valid'] and email_valid.context['is_unique']:
        context['is_valid'] = True


    return templates.TemplateResponse("auth/registration/submit.html", context) 