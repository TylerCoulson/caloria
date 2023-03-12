from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session  # type: ignore

from app import deps
from app.auth.router import get_current_profile
from app import schemas
from app import models

router = APIRouter()

from app import crud


@router.post(
    "",
    response_model=schemas.Profile,
    status_code=status.HTTP_201_CREATED,
)
async  def create_profile(*, profile: schemas.ProfileCreate, db: Session = Depends(deps.get_db)):
    profile_out = await crud.create(obj_in=profile, db=db, model=models.Profile)
    return profile_out

@router.get(
    "/me",
    response_model=schemas.ProfileLogs,
    status_code=status.HTTP_200_OK,
)
async def get_profile_id(*, profile: models.Profile = Depends(get_current_profile), db: Session = Depends(deps.get_db)):
    # data = await crud.read(_id=profile_id, db=db, model=models.Profile)
    return profile


@router.put(
    "/{profile_id}",
    response_model=schemas.ProfileLogs,
    status_code=status.HTTP_200_OK,
)
async def update_profile(
    *, profile_id: int, profile_in: schemas.ProfileBase, db: Session = Depends(deps.get_db)
):
    data = await get_profile_id(profile_id=profile_id, db=db)
    data = await crud.update(db_obj=data, data_in=profile_in, db=db)
    
    return data


@router.delete(
    "/{profile_id}",
    status_code=status.HTTP_200_OK,
)
async def delete_profile(*, profile_id: int, db: Session = Depends(deps.get_db)):
    data = await get_profile_id(profile_id=profile_id, db=db)

    data = await crud.delete(_id=profile_id, db=db, db_obj=data)
    return
