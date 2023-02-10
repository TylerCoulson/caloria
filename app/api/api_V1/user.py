from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session  # type: ignore

from app import deps
from app import schemas
from app import models

router = APIRouter()

from app import crud


@router.post(
    "",
    response_model=schemas.UserLogs,
    status_code=status.HTTP_201_CREATED,
)
def create_user(*, user: schemas.UserCreate, db: Session = Depends(deps.get_db)):
    if db.query(models.User).filter(models.User.email == user.email).first():
            raise HTTPException(status_code=403, detail="Email already has an account")
    user_out = crud.create(obj_in=user, db=db, model=models.User)
    return user_out

@router.get(
    "/{user_id}",
    response_model=schemas.UserLogs,
    status_code=status.HTTP_200_OK,
)
def get_user_id(*, user_id: int, db: Session = Depends(deps.get_db)):
    data = crud.read(_id=user_id, db=db, model=models.User)
    if not data:
        raise HTTPException(status_code=404, detail="User not found")
    return data



# @router.put(
#     "/{user_id}",
#     response_model=schemas.UserBase,
#     status_code=status.HTTP_200_OK,
# )
# def update_user(
#     *, user_id: int, user_in: schemas.UserBase, db: Session = Depends(deps.get_db)
# ):
#     data = get_user(user_id=user_id, db=db)

#     data = crud.update(db_obj=data, data_in=user_in, db=db)
#     return data


# @router.delete(
#     "/{user_id}",
#     status_code=status.HTTP_200_OK,
# )
# def delete_user(*, user_id: int, db: Session = Depends(deps.get_db)):
#     data = get_user(user_id=user_id, db=db)

#     data = crud.delete(_id=user_id, db=db, db_obj=data)
#     return data
