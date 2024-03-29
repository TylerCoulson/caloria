from fastapi import APIRouter, status, HTTPException
from sqlalchemy import select
from datetime import datetime, date
from app import schemas
from app import models
from app import crud

from app.api.calcs.weight_calcs import daily_log
from app.api.api_V1.deps import LoggedInDeps
from app.api.api_V1 import utils
router = APIRouter()


#  ************
#  *  CREATE  *
#  ************

@router.post(
    "",
    response_model=schemas.DailyOverview,
    status_code=status.HTTP_201_CREATED,
)
async def post_daily(*, deps:LoggedInDeps, actual_weight:bool=False, activity_level:bool=False, data: schemas.DailyOverviewInput):
    weight_data = await utils.get_weight(profile_id=deps['profile'].id, current_date=data.date, db=deps['db'])

    if weight_data is None:
        log = await crud.create(obj_in=data, db=deps['db'], model=models.DailyLog, profile=deps['profile'])
        output_data = await get_daily(deps=deps, current_date=log.date)

    else:
        data.activity_level = data.activity_level if activity_level else weight_data.activity_level
        data.actual_weight = data.actual_weight if actual_weight else weight_data.actual_weight 
        output_data = await update_daily(deps=deps, current_date=data.date, daily_data=data, actual_weight=actual_weight, activity_level=activity_level)

    return output_data

#  ************
#  *  READ  *
#  ************
@router.get(
    "",
    response_model=list[schemas.DailyOverview],
    status_code=status.HTTP_200_OK,
)
async def get_all_daily(*, deps:LoggedInDeps, n:int=25, page:int=1):
    if n < 0:
        n = 25

    offset = max((page-1) * n, 0)

    logs = await daily_log(profile=deps['profile'], db=deps['db'], end_date=deps['client_date'])
    return logs[offset:offset+n]
    

    
@router.get(
    "/{current_date}",
    response_model=schemas.DailyOverview,
    status_code=status.HTTP_200_OK,
)
async def get_daily(*, deps:LoggedInDeps, current_date:date):
    print(type(current_date), type(deps['profile'].start_date))
    if current_date < deps['profile'].start_date:
        raise HTTPException(status_code=404, detail="Date is before profile start date")
    
    output_data = await daily_log(profile=deps['profile'], db=deps['db'], end_date=current_date)
    
    for i in output_data:
        if i['date'] == current_date:
            return i
        else:
            continue


#  ************
#  *  UPDATE  *
#  ************
@router.put(
    "/{current_date}",
    response_model=schemas.DailyOverview,
    status_code=status.HTTP_200_OK,
)
async def update_daily(*, deps:LoggedInDeps, actual_weight:bool=False, activity_level:bool=False, current_date:date, daily_data:schemas.DailyOverviewInput):

    weight_data = await utils.get_weight(profile_id=deps['profile'].id, current_date=current_date, db=deps['db'])
    
    if weight_data is None:
        output_data = await post_daily(deps=deps, actual_weight=actual_weight, activity_level=activity_level, data=daily_data)
    else:
        daily_data.activity_level = daily_data.activity_level if activity_level else weight_data.activity_level
        daily_data.actual_weight = daily_data.actual_weight if actual_weight else weight_data.actual_weight
        data = await crud.update(_id=weight_data.id, model=models.DailyLog, update_data=daily_data, db=deps['db'], profile=deps['profile'])
        output_data = await get_daily(deps=deps, current_date=data.date)

    return output_data

# #  ************
# #  *  DELETE  *
# #  ************
# @router.delete(
#     "/{_id:int}",
#     status_code=status.HTTP_200_OK,
# )
# async def delete_daily_by_id(*, deps:LoggedInDeps, _id:int):
#     profile_id = deps['profile'].id
#     statement = select(models.DailyLog).where(models.DailyLog.profile_id == profile_id).where(models.DailyLog.id == _id)
#     weight_data = await deps['db'].execute(statement)
#     data = weight_data.unique().scalar_one_or_none()
#     await crud.delete(_id=data.id, db=deps['db'], db_obj=data)

# @router.delete(
#     "/{current_date}",
#     status_code=status.HTTP_200_OK,
# )
# async def delete_daily_by_date(*, deps:LoggedInDeps, current_date:date):
#     profile_id = deps['profile'].id
#     weight_data = await utils.get_weight(profile_id=profile_id, current_date=current_date, db=deps['db'])
#     await crud.delete(_id=weight_data.id, db=deps['db'], db_obj=weight_data)
#     return

