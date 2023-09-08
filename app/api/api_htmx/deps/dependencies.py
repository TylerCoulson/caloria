from fastapi import Depends, Request, Header
from sqlalchemy.orm import Session
from typing import Annotated

from app.auth.router import Annotated_User
from app import deps



async def common_deps(request: Request, profile: Annotated_User = False, hx_request: str | None = Header(default=None), db: Session = Depends(deps.get_db)):
    return {"request":request, "profile":profile, "hx_request":hx_request, "db":db}

CommonDeps = Annotated[dict, Depends(common_deps)]


async def logged_in_deps(common:CommonDeps, profile: Annotated_User):
    return {**common, "profile":profile}

LoggedInDeps = Annotated[dict, Depends(logged_in_deps)]