from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session  # type: ignore
from typing import List

from app import deps
from app import schemas
from app import models

from datetime import date
router = APIRouter()

from app import crud


@router.post(
    "",
    response_model=schemas.FoodLogProfile,
    status_code=status.HTTP_201_CREATED,
)
def post_food_log(*, food_log: schemas.FoodLogCreate, db: Session = Depends(deps.get_db)):
    food_log_out = crud.create(obj_in=food_log, db=db, model=models.Food_Log)
    return food_log_out

@router.get(
    "/{profile_id}/{date}",
    response_model=schemas.DayLog,
    status_code=status.HTTP_200_OK,
)
def get_food_log_date(*, date: date, profile_id:int, db: Session = Depends(deps.get_db)) -> list[schemas.FoodLogProfile]:
    data = db.query(models.Food_Log).filter(models.Food_Log.date == date).filter(models.Food_Log.profile_id == profile_id).all()
    profile = crud.read(_id=profile_id, db=db, model=models.Profile)

    if not data:
        raise HTTPException(status_code=404, detail="Food_log not found")
    return {"profile":profile, "log":data}

@router.get(
    "/{food_log_id}",
    response_model=schemas.FoodLogProfile,
    status_code=status.HTTP_200_OK,
)
def get_food_log_id(*, food_log_id: int, db: Session = Depends(deps.get_db)):
    data = crud.read(_id=food_log_id, db=db, model=models.Food_Log)
    if not data:
        raise HTTPException(status_code=404, detail="Food_log not found")
    return data

@router.get(
    "",
    response_model=schemas.FoodLog,
    status_code=status.HTTP_200_OK,
)
def get_food_logs(*, profile_id:int, db: Session = Depends(deps.get_db)):
    data = db.query(models.Food_Log).filter(models.Food_Log.profile_id == profile_id).all()

    return data

@router.put(
    "/{food_log_id}",
    response_model=schemas.FoodLog,
    status_code=status.HTTP_200_OK,
)
def update_food_log(
    *, food_log_id: int, food_log_in: schemas.FoodLogBase, db: Session = Depends(deps.get_db)
):
    data = get_food_log_id(food_log_id=food_log_id, db=db)

    data = crud.update(db_obj=data, data_in=food_log_in, db=db)
    return data


@router.delete(
    "/{food_log_id}",
    status_code=status.HTTP_200_OK,
)
def delete_food_log(*, food_log_id: int, db: Session = Depends(deps.get_db)):
    data = get_food_log_id(food_log_id=food_log_id, db=db)

    data = crud.delete(_id=food_log_id, db=db, db_obj=data)
    return
