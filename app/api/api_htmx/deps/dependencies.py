from datetime import datetime, timedelta
from fastapi import Depends, Request, Header
from sqlalchemy.orm import Session
from typing import Annotated

from app.auth.router import Annotated_Profile, Annotated_User
from app import deps



async def common_deps(request: Request, user: Annotated_User = False, hx_request: str | None = Header(default=None), db: Session = Depends(deps.get_db), timezone_offset: int = 0):
    client_date = (datetime.now() - timedelta(minutes=timezone_offset)).date()
    return {"request":request, "user":user, "hx_request":hx_request, "db":db, "client_date":client_date}

CommonDeps = Annotated[dict, Depends(common_deps)]


async def logged_in_deps(common:CommonDeps, profile: Annotated_Profile):
    return {**common, "profile":profile}

LoggedInDeps = Annotated[dict, Depends(logged_in_deps)]