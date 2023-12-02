from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from app.auth.db import get_user_db
from app.auth.schemas import UserCreate
from app.auth.users import get_user_manager

router = APIRouter(prefix='/validate')
templates = Jinja2Templates("app/templates")

@router.get(
    "/password",
    response_class=HTMLResponse,
    status_code=status.HTTP_200_OK,
)
async def validate_password(email:str, password:str, manager = Depends(get_user_manager)):
    user = UserCreate(email=email, password=password)
    await manager.validate_password(user.password, user)
    return

@router.get(
    "/password_confirm",
    response_class=HTMLResponse,
    status_code=status.HTTP_200_OK,
)
def confirm_password(password:str, password_confirm:str):
    is_valid = password == password_confirm 
    
    if is_valid:
        return 
    raise HTTPException(status_code=400, detail="PASSWORD_PASSWORD_CONFIRM_DO_NOT_MATCH")

@router.get(
    "/email",
    response_class=HTMLResponse,
    status_code=status.HTTP_200_OK,
)
async def validate_email(*, email:str, db = Depends(get_user_db)):
    existing_user = await db.get_by_email(email)
    
    if existing_user is not None:
        raise HTTPException(status_code=400, detail="REGISTER_USER_ALREADY_EXISTS")
    return 