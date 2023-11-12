from fastapi import Depends, Request, Header
from sqlalchemy.orm import Session
from typing import Annotated

from app.auth.router import Annotated_Profile, Annotated_User
from app import deps, schemas



async def common_deps(user: Annotated_User = False, db: Session = Depends(deps.get_db)):
    return {"user":user, "db":db}

CommonDeps = Annotated[dict, Depends(common_deps)]


async def logged_in_deps(common:CommonDeps, profile: Annotated_Profile):
    return {**common, "profile": schemas.Profile(**profile.__dict__)}

LoggedInDeps = Annotated[dict, Depends(logged_in_deps)]