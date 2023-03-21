from fastapi import APIRouter, Depends, status, Request, Header
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
    return f'''
        <div class='form-group valid' hx-target="this" hx-swap="outerHTML">
            <label for="password">Password:</label>
            <input class='form-control' type="password" id="password" name="password" hx-include='#email' value={user.password} hx-get="/validate/password">
        </div>
    '''

@router.get(
    "/password_confirm",
    response_class=HTMLResponse,
    status_code=status.HTTP_200_OK,
)
def confirm_password(password:str, password_confirm:str):
    is_valid = password == password_confirm 
    
    if is_valid:
        return f'''
            <div class='form-group valid' hx-target="this" hx-swap="outerHTML">
                <label for="password">Confirm Password:</label>
                <input class='form-control' type="password" id="password_confirm" name="password_confirm" value={password_confirm} hx-include="#password" hx-get="/validate/password_confirm">
            </div>
        '''
    return f'''
            <div class='form-group is-invalid' hx-target="this" hx-swap="outerHTML">
                <label for="password">Confirm Password:</label>
                <input class='form-control' type="password" id="password_confirm" name="password_confirm" value={password_confirm} hx-include="#password" hx-get="/validate/password_confirm">
                <div class='invalid-feedback'>Passwords do not match</div>
            </div>
        '''

@router.get(
    "/email",
    response_class=HTMLResponse,
    status_code=status.HTTP_200_OK,
)
async def validate_email(*, email:str, db = Depends(get_user_db)):
    existing_user = await db.get_by_email(email)
    
    if existing_user is not None:
        return f'''
            <div hx-target="this" hx-swap=""outerHTML>
                <label for="email">Email:</label>
                <input type="text" id="email" name="email" hx-get="/validate/email" value="{email}" required minlength="2" pattern=".+@.+\..+" aria-invalid="true">
                <div class='warning'>This email is already taken</div>
            </div>
        '''
    return f'''
            <div class='form-group valid' hx-target="this" hx-swap=""outerHTML>
                <label for="email">Email:</label>
                <input class='form-control' type="text" id="email" name="email" hx-get="/validate/email" value="{email}" required minlength="2" pattern=".+@.+\..+" aria-invalid="false">
            </div>
        '''
    