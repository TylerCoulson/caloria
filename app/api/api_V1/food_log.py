# from fastapi import APIRouter, status, HTTPException
# from sqlalchemy import select, and_
# from typing import List

# from app.api.api_V1.deps import LoggedInDeps
# from app import schemas
# from app import models

# from datetime import date
# router = APIRouter()

# from app import crud

# @router.post(
#     "",
#     response_model=schemas.FoodLogProfile,
#     status_code=status.HTTP_201_CREATED,
# )
# async def post_food_log(*, deps:LoggedInDeps, food_log: schemas.FoodLogCreate):

#     food_log_out = await crud.create(obj_in=food_log, db=deps['db'], model=models.Food_Log, profile=deps['profile'] )
#     return food_log_out

# @router.get(
#     "/date/{date}",
#     response_model=schemas.DayLog,
#     status_code=status.HTTP_200_OK,
# )
# async def get_food_log_date(*, deps:LoggedInDeps, date: date, n:int=25, page:int=1) -> list[schemas.FoodLogProfile]:
#     if n < 0:
#         n = 25

#     offset = max((page-1) * n, 0)
#     statement = select(models.Food_Log).where(models.Food_Log.profile_id == deps['profile'].id).where(models.Food_Log.date == date).limit(n).offset(offset)
#     data = await deps['db'].execute(statement)

#     profile = await crud.read(_id=deps['profile'].id, db=deps['db'], model=models.Profile)
#     return {"profile":profile, "log":[value for value, in data.unique().all()]}

# @router.get(
#     "/{food_log_id}",
#     response_model=schemas.FoodLogProfile,
#     status_code=status.HTTP_200_OK,
# )
# async def get_food_log_id(*, deps:LoggedInDeps, food_log_id: int):
#     data = await crud.read(_id=food_log_id, db=deps['db'], model=models.Food_Log)
#     if not data:
#         raise HTTPException(status_code=404, detail="Food_log not found")
#     return data

# @router.get(
#     "",
#     response_model=List[schemas.FoodLog],
#     status_code=status.HTTP_200_OK,
# )
# async def get_food_logs(*, deps:LoggedInDeps, n:int=25, page:int=1):
#     if n < 0:
#         n = 25

#     offset = max((page-1) * n, 0)
#     profile_id = deps['profile'].id
#     start_date = deps['profile'].start_date
#     statement = select(models.Food_Log
#         ).where(
#             and_(
#                     models.Food_Log.profile_id == profile_id, 
#                     models.Food_Log.date >= start_date
#                 )
#         ).order_by(models.Food_Log.date.desc()
#         ).order_by(models.Food_Log.id.desc()
#         ).limit(n
#         ).offset(offset
#                                            )
#     data = await deps['db'].execute(statement)
#     test = data.unique().all()

#     return [value for value, in test]

# @router.put(
#     "/{food_log_id}",
#     response_model=schemas.FoodLogProfile,
#     status_code=status.HTTP_200_OK,
# )
# async def update_food_log(*, deps:LoggedInDeps, food_log_id: int, food_log_in: schemas.FoodLogBase):
    
#     data = await crud.update(_id=food_log_id, model=models.Food_Log, update_data=food_log_in, db=deps['db'], profile=deps['profile'])
    
#     return data


# @router.delete(
#     "/{food_log_id}",
#     status_code=status.HTTP_200_OK,
# )
# async def delete_food_log(*, deps:LoggedInDeps, food_log_id: int):
#     data = await get_food_log_id(deps=deps, food_log_id=food_log_id)

#     data = await crud.delete(_id=food_log_id, db=deps['db'], db_obj=data)
#     return
