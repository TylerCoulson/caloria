from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session  # type: ignore

from app import deps
from app import schemas
from app import models

router = APIRouter()

from app import crud


@router.post(
    "",
    response_model=schemas.ProfileLogs,
    status_code=status.HTTP_201_CREATED,
)
def create_profile(*, profile: schemas.ProfileCreate, db: Session = Depends(deps.get_db)):
    if db.query(models.Profile).filter(models.Profile.email == profile.email).first():
            raise HTTPException(status_code=403, detail="Email already has an account")
    profile_out = crud.create(obj_in=profile, db=db, model=models.Profile)
    return profile_out

@router.get(
    "/{profile_id}",
    response_model=schemas.ProfileLogs,
    status_code=status.HTTP_200_OK,
)
def get_profile_id(*, profile_id: int, db: Session = Depends(deps.get_db)):
    data = crud.read(_id=profile_id, db=db, model=models.Profile)
    if not data:
        raise HTTPException(status_code=404, detail="Profile not found")
    return data



@router.put(
    "/{profile_id}",
    response_model=schemas.Profile,
    status_code=status.HTTP_200_OK,
)
def update_profile(
    *, profile_id: int, profile_in: schemas.ProfileBase, db: Session = Depends(deps.get_db)
):
    data = get_profile_id(profile_id=profile_id, db=db)

    data = crud.update(db_obj=data, data_in=profile_in, db=db)
    return data


@router.delete(
    "/{profile_id}",
    status_code=status.HTTP_200_OK,
)
def delete_profile(*, profile_id: int, db: Session = Depends(deps.get_db)):
    data = get_profile_id(profile_id=profile_id, db=db)

    data = crud.delete(_id=profile_id, db=db, db_obj=data)
    return
