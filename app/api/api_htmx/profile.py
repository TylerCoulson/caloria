from fastapi import APIRouter, Depends, status, Request, HTTPException, Header
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session  # type: ignore
from fastapi.templating import Jinja2Templates
from fastapi.encoders import jsonable_encoder

from app import deps
from app import schemas
from app import models
from app.api.api_V1 import profile as api_profile

router = APIRouter()
templates = Jinja2Templates("app/templates")

@router.post(
    "",
    response_class=HTMLResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_profile(*, request: Request,hx_request: str | None = Header(default=None), profile: schemas.ProfileCreate, db: Session = Depends(deps.get_db)):
    food_out = jsonable_encoder(api_profile.create_profile(profile=profile, db=db))
    # food_out = [schemas.FoodBase(**jsonable_encoder(food_db))]

    context = {
            "request": request,
            "hx_request": hx_request,
            "profile": [food_out]
        }
    return templates.TemplateResponse("profile.html", context)

@router.get(
    "",
    response_class=HTMLResponse,
    status_code=status.HTTP_200_OK,
)
def get_profile(*, request: Request,hx_request: str | None = Header(default=None), profile_id: int, db: Session = Depends(deps.get_db)):
    try:
        profile_out = jsonable_encoder(api_profile.get_profile_id(profile_id=profile_id, db=db))

        context = {
                "request": request,
                "hx_request": hx_request,
                "profile": profile_out
            }

        return templates.TemplateResponse("profile.html", context)

    except HTTPException:
        context = {
            "request": request,
            "hx_request": hx_request,
            "message": f"Profile with id {profile_id} does not exist"
        }
        return templates.TemplateResponse("404.html", context)