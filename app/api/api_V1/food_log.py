from fastapi import APIRouter, status, HTTPException
from sqlalchemy import select, and_
from typing import List

from app.api.api_V1.deps import LoggedInDeps
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
async def post_food_log(*, deps:LoggedInDeps, food_log: schemas.FoodLogCreate):
    food_log_out = await crud.create(obj_in=food_log, db=deps['db'], model=models.Food_Log, profile=deps['profile'] )
    return food_log_out

@router.get(
    "/date/{date}",
    response_model=schemas.DayLog,
    status_code=status.HTTP_200_OK,
)
async def get_food_log_date(*, deps:LoggedInDeps, date: date, n:int=25, page:int=1) -> list[schemas.FoodLogProfile]:
    statement = await crud.read_all_statement(n=n, page=page, db=deps['db'], model=models.Food_Log, profile=deps['profile'])
    statement = statement.where(models.Food_Log.date == date)
    data = await deps['db'].execute(statement)


    return {"profile":deps['profile'], "log":[value for value, in data.unique().all()]}

@router.get(
    "/{food_log_id}",
    response_model=schemas.FoodLogProfile,
    status_code=status.HTTP_200_OK,
)
async def get_food_log_id(*, deps:LoggedInDeps, food_log_id: int):
    data = await crud.read(_id=food_log_id, db=deps['db'], model=models.Food_Log, profile=deps['profile'])
    if not data:
        raise HTTPException(status_code=404, detail="Food_log not found")
    return data

@router.get(
    "",
    response_model=List[schemas.FoodLog],
    status_code=status.HTTP_200_OK,
)
async def get_food_logs(*, deps:LoggedInDeps, n:int=25, page:int=1):

    if n < 0:
        n = 25

    offset = max((page-1) * n, 0)
    profile_id = deps['profile'].id
    start_date = deps['profile'].start_date
    statement = await crud.read_all_statement(n=n, page=page, db=deps['db'], model=models.Food_Log, profile=deps['profile'])
    
    statement = statement.where(
    and_(
            models.Food_Log.profile_id == profile_id, 
            models.Food_Log.date >= start_date
        )
    ).order_by(models.Food_Log.date.desc()
    ).order_by(models.Food_Log.id.desc()
    )

    data = await deps['db'].execute(statement)
    test = data.unique().all()
    return [value for value, in test]

@router.put(
    "/{food_log_id}",
    response_model=schemas.FoodLogProfile,
    status_code=status.HTTP_200_OK,
)
async def update_food_log(*, deps:LoggedInDeps, food_log_id: int, food_log_in: schemas.FoodLogBase):
    
    data = await crud.update(_id=food_log_id, model=models.Food_Log, update_data=food_log_in, db=deps['db'], profile=deps['profile'])
    if data is None:
        raise HTTPException(status_code=404, detail="Cannot Update Log")
    return data


@router.delete(
    "/{food_log_id}",
    status_code=status.HTTP_200_OK,
)
async def delete_food_log(*, deps:LoggedInDeps, food_log_id: int):
    data = await crud.delete(_id=food_log_id, db=deps['db'], model=models.Food_Log, profile=deps['profile'])
    if data is None:
        raise HTTPException(status_code=404, detail="Cannot Delete Log")
    return
