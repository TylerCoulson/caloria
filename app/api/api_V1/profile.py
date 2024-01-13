from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session  # type: ignore

from app import deps
from app.auth.router import Annotated_Profile, current_active_user
from app import schemas
from app import models
from app.api.api_V1.deps import CommonDeps, LoggedInDeps
router = APIRouter()

from app import crud

#  ************
#  *  CREATE  *
#  ************
@router.post(
    "",
    response_model=schemas.Profile,
    status_code=status.HTTP_201_CREATED,
)
async  def create_profile(*, deps:CommonDeps, profile: schemas.ProfileBase, user:dict=Depends(current_active_user)):
    
    profile = schemas.ProfileCreate(**profile.model_dump(), user_id=user.id) 
    profile_out = await crud.create(obj_in=profile, db=deps['db'], model=models.Profile)
    return profile_out


#  ************
#  *   Read   *
#  ************
@router.get(
    "/me",
    response_model=schemas.Profile,
    status_code=status.HTTP_200_OK,
)
async def get_current_profile(*, deps:LoggedInDeps):
    data = await crud.read(_id=deps['profile'].id, db=deps['db'], model=models.Profile, profile=deps['profile'])
    print(data)
    return data

# @router.get(
#     "/all",
#     # response_model=schemas.UserRead,
#     status_code=status.HTTP_200_OK,
# )
# async def get_user(*, deps:LoggedInDeps):
#     data = await crud.read_all(db=deps['db'], model=models.User)
#     return data

@router.get(
    "/me/logs",
    response_model=schemas.ProfileLogs,
    status_code=status.HTTP_200_OK,
)
async def get_current_profile_logs(*, deps:LoggedInDeps):
    data = await crud.read(_id=deps['profile'].id, db=deps['db'], model=models.Profile, profile=deps['profile'])
    return data


#  ************
#  *  Update  *
#  ************
@router.put(
    "/me",
    response_model=schemas.Profile,
    status_code=status.HTTP_200_OK,
)
async def update_current_profile(*, deps:LoggedInDeps, profile_in: schemas.ProfileBase):
    data = await crud.update(_id=deps['profile'].id, model=models.Profile, update_data=profile_in, db=deps['db'], profile=deps['profile'])
    return data


#  ************
#  *  DELETE  *
#  ************

@router.delete(
    "/me",
    status_code=status.HTTP_200_OK,
)
async def delete_current_profile(*, deps:LoggedInDeps):
    data = await crud.delete(_id=deps['profile'].id, db=deps['db'], model=models.Profile, profile=deps['profile'])
    print("delete output", data)
    if data is None:
        raise HTTPException(status_code=404, detail="Cannot Delete Profile")
    return
