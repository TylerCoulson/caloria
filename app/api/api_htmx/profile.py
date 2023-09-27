from fastapi import APIRouter, Depends, status, Request, HTTPException, Header
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session  # type: ignore
from fastapi.templating import Jinja2Templates
from fastapi.encoders import jsonable_encoder

from app import deps
from app import schemas
from app import models
from app.api.api_V1 import profile as api_profile
from app.api.api_htmx.deps import LoggedInDeps, CommonDeps
from app.auth.router import current_active_user

router = APIRouter(prefix="/profile")
templates = Jinja2Templates("app/templates")

@router.put(
    "",
    response_class=HTMLResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_profile(*, deps:CommonDeps, profile: schemas.ProfileBase, user:dict=Depends(current_active_user)):
    if user.profile is None:
        profile = await api_profile.create_profile(deps=deps, profile=profile, user=user)
    else:
        deps['profile'] = user.profile
        profile = await api_profile.update_current_profile(deps=deps, profile_in=profile)
    context = {
            "request": deps['request'],
            "hx_request": deps['hx_request'],
            "profile": profile
        }
    return templates.TemplateResponse("profile/profile.html", context)

@router.get(
    "",
    response_class=HTMLResponse,
    status_code=status.HTTP_200_OK,
)
async def get_profile(*, deps:LoggedInDeps):
    context = {
            "request": deps['request'],
            "hx_request": deps['hx_request'],
            "profile": deps['profile']
        }

    return templates.TemplateResponse("profile/profile.html", context)

@router.get(
    "/edit",
    response_class=HTMLResponse,
    status_code=status.HTTP_200_OK,
)
async def edit_profile(*, deps:LoggedInDeps):
    print(deps['request'].url)
    context = {
            "request": deps['request'],
            "hx_request": deps['hx_request'],
            "profile": deps['profile']
        }

    return templates.TemplateResponse("profile/create_profile.html", context)

@router.get(
    "/create",
    response_class=HTMLResponse,
    status_code=status.HTTP_200_OK,
)
def create_profile(*, request: Request, hx_request: str | None = Header(default=None)):
    context = {
            "request": request,
            "hx_request": hx_request
        }

    return templates.TemplateResponse("profile/create_profile.html", context)