from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy import select, func, extract, cast, Integer, Numeric, or_, column, Date, Interval, Text
from sqlalchemy.orm import Session  # type: ignore
from datetime import datetime, date
from app import deps
from app import schemas
from app import models
from app import crud

from app.api.calcs.weight_calcs import daily_log
from app.api.calcs.calorie_calcs import PersonsDay 
from app.auth.router import Annotated_Profile
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
async def post_daily(*, actual_weight: schemas.DailyOverviewInput, profile: Annotated_Profile, db: Session = Depends(deps.get_db)):
    actual_weight.profile_id = profile.id
    log = await crud.create(obj_in=actual_weight, db=db, model=models.DailyLog)
    output_data = await get_daily(profile=profile, current_date=log.date, db=db)
    return output_data

@router.get(
    "",
    response_model=list[schemas.DailyOverview],
    status_code=status.HTTP_200_OK,
)
async def get_all_daily(*, profile: Annotated_Profile, n:int=25, page:int=1, db: Session = Depends(deps.get_db)):
    offset = max((page-1) * n, 0)
    logs = await daily_log(profile=profile, db=db)
    return logs[offset:offset+n]
    

    
@router.get(
    "/{current_date}",
    response_model=schemas.DailyOverview,
    status_code=status.HTTP_200_OK,
)
async def get_daily(*, profile: Annotated_Profile, current_date:date, db: Session = Depends(deps.get_db)):
    start_date = datetime.strptime(profile.start_date, '%Y-%m-%d').date()
    print(current_date, start_date, start_date == current_date)
    if current_date < start_date:
        raise HTTPException(status_code=404, detail="Date is before profile start date")
    
    output_data = await daily_log(profile=profile, db=db)
    
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
async def update_daily(
    *, profile: Annotated_Profile, current_date:date, daily_data:schemas.DailyOverviewInput, db: Session = Depends(deps.get_db)
):
    daily_data.profile_id = profile.id
    weight_data = await get_weight(profile_id=profile.id, current_date=current_date, db=db)
    if weight_data is None:
        output_data = await post_daily(actual_weight=daily_data, profile=profile, db=db)
    else:
        data = await crud.update(_id=weight_data.id, model=models.DailyLog, update_data=daily_data, db=db)
        output_data = await get_daily(profile=profile, current_date=data.date, db=db)
    return output_data

@router.delete(
    "/{_id:int}",
    status_code=status.HTTP_200_OK,
)
async def delete_daily_by_id(*, profile: Annotated_Profile, _id:int, db: Session = Depends(deps.get_db)):
    profile_id = profile.id
    statement = select(models.DailyLog).where(models.DailyLog.profile_id == profile_id).where(models.DailyLog.id == _id)
    weight_data = await db.execute(statement)
    data = weight_data.unique().scalar_one_or_none()
    await crud.delete(_id=data.id, db=db, db_obj=data)

@router.delete(
    "/{current_date}",
    status_code=status.HTTP_200_OK,
)
async def delete_daily_by_date(*, profile: Annotated_Profile, current_date:date, db: Session = Depends(deps.get_db)):
    profile_id = profile.id
    weight_data = await get_weight(profile_id=profile_id, current_date=current_date, db=db)
    await crud.delete(_id=weight_data.id, db=db, db_obj=weight_data)
    return

