from fastapi import APIRouter, status, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session  # type: ignore
from datetime import datetime, date
from app import schemas
from app import models
from app import crud

from app.api.calcs.weight_calcs import daily_log
from app.api.api_V1.deps import LoggedInDeps
router = APIRouter()


async def get_weight(profile_id, current_date, db: Session):
    statement = select(models.DailyLog).where(models.DailyLog.profile_id == profile_id).where(models.DailyLog.date == current_date)
    data = await db.execute(statement)
    return data.unique().scalar_one_or_none()



@router.post(
    "",
    response_model=schemas.DailyOverview,
    status_code=status.HTTP_201_CREATED,
)
async def post_daily(*, deps:LoggedInDeps, actual_weight: schemas.DailyOverviewInput):
    actual_weight.profile_id = deps['profile'].id
    log = await crud.create(obj_in=actual_weight, db=deps['db'], model=models.DailyLog)
    output_data = await get_daily(deps=deps, current_date=log.date)
    return output_data

@router.get(
    "",
    response_model=list[schemas.DailyOverview],
    status_code=status.HTTP_200_OK,
)
async def get_all_daily(*, deps:LoggedInDeps, n:int=25, page:int=1):
    offset = max((page-1) * n, 0)
    logs = await daily_log(profile=deps['profile'], db=deps['db'])
    return logs[offset:offset+n]
    

    
@router.get(
    "/{current_date}",
    response_model=schemas.DailyOverview,
    status_code=status.HTTP_200_OK,
)
async def get_daily(*, deps:LoggedInDeps, current_date:date):
    start_date = deps['profile'].start_date if type(deps['profile'].start_date) is date else datetime.strptime(deps['profile'].start_date, '%Y-%m-%d').date()
    if current_date < start_date:
        raise HTTPException(status_code=404, detail="Date is before profile start date")
    
    output_data = await daily_log(profile=deps['profile'], db=deps['db'])
    
    for i in output_data:
        if i['date'] == current_date:
            return i
        else:
            continue


@router.put(
    "/{current_date}",
    response_model=schemas.DailyOverview,
    status_code=status.HTTP_200_OK,
)
async def update_daily(*, deps:LoggedInDeps, current_date:date, daily_data:schemas.DailyOverviewInput):
    
    daily_data.profile_id = deps['profile'].id
    weight_data = await get_weight(profile_id=deps['profile'].id, current_date=current_date, db=deps['db'])
    if weight_data is None:
        output_data = await post_daily(actual_weight=daily_data, profile=deps['profile'], db=deps['db'])
    else:
        data = await crud.update(_id=weight_data.id, model=models.DailyLog, update_data=daily_data, db=deps['db'])
        output_data = await get_daily(deps=deps, current_date=data.date)
    return output_data

@router.delete(
    "/{_id:int}",
    status_code=status.HTTP_200_OK,
)
async def delete_daily_by_id(*, deps:LoggedInDeps, _id:int):
    profile_id = deps['profile'].id
    statement = select(models.DailyLog).where(models.DailyLog.profile_id == profile_id).where(models.DailyLog.id == _id)
    weight_data = await deps['db'].execute(statement)
    data = weight_data.unique().scalar_one_or_none()
    await crud.delete(_id=data.id, db=deps['db'], db_obj=data)

@router.delete(
    "/{current_date}",
    status_code=status.HTTP_200_OK,
)
async def delete_daily_by_date(*, deps:LoggedInDeps, current_date:date):
    profile_id = deps['profile'].id
    weight_data = await get_weight(profile_id=profile_id, current_date=current_date, db=deps['db'])
    await crud.delete(_id=weight_data.id, db=deps['db'], db_obj=weight_data)
    return

