from datetime import datetime, timedelta
from fastapi import Depends, Request, Header
from sqlalchemy.orm import Session
from typing import Annotated

from app.auth.router import Annotated_Profile, Annotated_User
from app import deps, schemas



async def common_deps(user: Annotated_User = False, db: Session = Depends(deps.get_db), timezone_offset: int = 0, profile:Annotated_Profile=False):
    client_date = (datetime.now() - timedelta(minutes=timezone_offset)).date()  
    return {"user":user, "db":db, "client_date": client_date, "profile": profile}

CommonDeps = Annotated[dict, Depends(common_deps)]


async def logged_in_deps(common:CommonDeps, profile: Annotated_Profile):
    return {**common, "profile": schemas.Profile(**profile.__dict__)}

LoggedInDeps = Annotated[dict, Depends(logged_in_deps)]