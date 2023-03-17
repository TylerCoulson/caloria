from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session  # type: ignore
from datetime import date, timedelta
from app import deps
from app import schemas
from app import models
from app import crud

from app.api.calcs.calorie_calcs import PersonsDay 
from app.auth.router import get_current_profile
router = APIRouter()


async def get_weight(profile_id, current_date, db):
    statement = select(models.DailyLog).where(models.DailyLog.profile_id == profile_id).where(models.DailyLog.date == current_date)
    data = await db.execute(statement)
    return data.unique().scalar_one_or_none()

async def daily_log(profile_id:int, current_date:date, db):
    profile_data = await crud.read(_id=profile_id, db=db, model=models.Profile)

    log_data = PersonsDay(height=profile_data.height, start_weight=profile_data.start_weight, start_date=profile_data.start_date, lbs_per_day=(profile_data.lbs_per_week/7), birthdate=profile_data.birthdate, sex=profile_data.sex, activity_level=profile_data.activity_level, goal_weight=profile_data.goal_weight, profile_logs=profile_data.log) 

    profile_age = log_data.age(current_date)
    day = (current_date - profile_data.start_date).days
    est_weight = log_data.estimated_weight(current_date=current_date)
    current_rmr  = log_data.resting_rate(weight=est_weight, age=profile_age)
    calories_eaten_on_current_date = log_data.calories_eaten_today()
    calorie_goal = log_data.calorie_goal(weight=est_weight, age=log_data.age(current_date))
    total_lbs_lost = log_data.total_lbs_lost(current_date=current_date)
    total_calorie_surplus = log_data.calorie_surplus(current_date=current_date)
    weight_data = await get_weight(profile_id=profile_id, current_date=current_date, db=db)

    output_data = {
        "date": current_date,
        "profile_id":profile_id,
        'day':day,
        'week':(day//7)+1,
        'est_weight':est_weight,
        'resting_rate':current_rmr,
        'eaten_calories':calories_eaten_on_current_date,
        'calorie_goal':calorie_goal,
        'total_lbs_lost':total_lbs_lost,
        'calorie_surplus':total_calorie_surplus,
        'calories_left':calorie_goal - calories_eaten_on_current_date,
        'bmi':log_data.bmi(current_date=current_date),
        'actual_weight':weight_data.actual_weight if weight_data else 0
    }
    return output_data

@router.post(
    "",
    response_model=schemas.DailyOverview,
    status_code=status.HTTP_201_CREATED,
)
async def post_daily(*, actual_weight: schemas.DailyOverviewInput, profile: models.Profile = Depends(get_current_profile), db: Session = Depends(deps.get_db)):
    actual_weight.profile_id = profile.id
    log = await crud.create(obj_in=actual_weight, db=db, model=models.DailyLog)
    
    output_data = await daily_log(profile_id=log.profile_id, current_date=log.date, db=db)
    return output_data

@router.get(
    "",
    response_model=schemas.DailyOverview,
    status_code=status.HTTP_200_OK,
)
async def get_all_daily(*, profile: models.Profile = Depends(get_current_profile), n_days:int=50, db: Session = Depends(deps.get_db)):
    profile_id = profile.id
    output_data = []
    current_date = date.today()
    start_date = profile.start_date
    total_days = (current_date - start_date).days
    
    for i in range(min(total_days, n_days)+1):
        i_date = current_date - timedelta(i)
        output_data.append( await daily_log(profile_id=profile_id, current_date=i_date, db=db))
    
    return output_data

@router.get(
    "/{current_date}",
    response_model=schemas.DailyOverview,
    status_code=status.HTTP_200_OK,
)
async def get_daily(*, profile: models.Profile = Depends(get_current_profile), current_date:date, db: Session = Depends(deps.get_db)):
    profile_id = profile.id
    output_data = await daily_log(profile_id=profile_id, current_date=current_date, db=db)

    return output_data

@router.put(
    "/{current_date}",
    response_model=schemas.DailyOverview,
    status_code=status.HTTP_200_OK,
)
async def update_daily(
    *, profile: models.Profile = Depends(get_current_profile), current_date:date, daily_data:schemas.DailyOverviewInput, db: Session = Depends(deps.get_db)
):
    profile_id = profile.id
    weight_data = await get_weight(profile_id=profile_id, current_date=current_date, db=db)

    data = await crud.update(db_obj=weight_data, data_in=daily_data, db=db)
    
    output = await daily_log(profile_id, current_date, db)

    return output


@router.delete(
    "/{current_date}",
    status_code=status.HTTP_200_OK,
)
async def delete_food(*, profile: models.Profile = Depends(get_current_profile), current_date:date, db: Session = Depends(deps.get_db)):
    profile_id = profile.id
    weight_data = await get_weight(profile_id=profile_id, current_date=current_date, db=db)
    await crud.delete(_id=weight_data.id, db=db, db_obj=weight_data)
    return
