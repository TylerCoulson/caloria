from fastapi import APIRouter, status
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from app.api.api_htmx.deps import CommonDeps

router = APIRouter(prefix='')
templates = Jinja2Templates("app/templates")

@router.get(
    "/verify",
    response_class=HTMLResponse,
    status_code=status.HTTP_200_OK,
)
async def verify_user(deps:CommonDeps, token:str = None):
    context = {
        "request": deps['request'],
        "hx_request": deps['hx_request'],
        "user": deps['user'],
        "verification": True,
        "token": token
    }
    
    return templates.TemplateResponse("index/index.html", context)