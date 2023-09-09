from fastapi import APIRouter, Depends, status, Request, HTTPException, Header
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session  # type: ignore
from fastapi.templating import Jinja2Templates
from fastapi.encoders import jsonable_encoder

from app import deps
from app import schemas
from app import models
from app.api.api_V1 import profile as api_profile
from app.api.api_htmx.deps import LoggedInDeps


router = APIRouter(prefix="/profile")
templates = Jinja2Templates("app/templates")

@router.post(
    "",
    response_class=HTMLResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_profile(*, deps:LoggedInDeps, profile: schemas.ProfileBase, db: Session = Depends(deps.get_db)):
    profile = await api_profile.create_profile(profile=profile, user=deps['profile'], db=db)

    context = {
            "request": deps['request'],
            "hx_request": deps['hx_request'],
            "profile": profile
        }
    return templates.TemplateResponse("profile.html", context)

@router.get(
    "",
    response_class=HTMLResponse,
    status_code=status.HTTP_200_OK,
)
async def get_profile(*, deps:LoggedInDeps):
    try:
        profile_out = await api_profile.get_current_profile(profile=deps['profile'], db=deps['db'])

        context = {
                "request": deps['request'],
                "hx_request": deps['hx_request'],
                "profile": profile_out
            }

        return templates.TemplateResponse("profile.html", context)

    except HTTPException:
        context = {
            "request": deps['request'],
            "hx_request": deps['hx_request'],
            "message": f"Profile with id {deps['profile'].id} does not exist"
        }
        return templates.TemplateResponse("404.html", context)