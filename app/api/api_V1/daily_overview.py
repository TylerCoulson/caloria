from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy import select, func, extract, cast, Integer, distinct
from sqlalchemy.orm import Session  # type: ignore
from datetime import date, timedelta
from app import deps
from app import schemas
from app import models
from app import crud
import time

from app.api.calcs.calorie_calcs import PersonsDay 
from app.auth.router import Annotated_Profile
router = APIRouter()


async def get_weight(profile_id, current_date, db: Session):
    statement = select(models.DailyLog).where(models.DailyLog.profile_id == profile_id).where(models.DailyLog.date == current_date)
    data = await db.execute(statement)
    return data.unique().scalar_one_or_none()

async def daily_log(profile:models.Profile, db: Session):
    profile_id = profile.id

    statement = select(
        models.Food_Log.date,
        func.sum(func.round(models.ServingSize.calories * models.Food_Log.serving_amount,0)).over(order_by=models.Food_Log.date), # total_calories_eaten
        (models.Profile.height*2.54) * 6.25, #height
        cast((extract('epoch', models.Food_Log.date) - extract('epoch', models.Profile.birthdate))/60/60/24/365.25, Integer) * 5, #age
        -161 if models.Profile.sex == 'female' else 5, #sex
        models.Profile.activity_level, #activity level
        cast((extract('epoch', models.Food_Log.date) - extract('epoch', models.Profile.start_date))/60/60/24, Integer)+1,
        models.Profile.lbs_per_week * 500,
        12000 if models.Profile.sex == 'female' else 1500,
        models.Profile.height * models.Profile.height,
        models.DailyLog.actual_weight
    ).where(models.Food_Log.profile_id == profile_id
    ).join(models.ServingSize
    ).join(models.Profile
    ).join(models.DailyLog, models.DailyLog.date == models.Food_Log.date, full=True,
    )
    
    data = await db.execute(statement)
    logs = []
    
    total_rmr = 0
    est_weight = profile.start_weight
    total_calorie_goal = 0
    previous_total_eaten = 0
    
    for i in data.unique().all():
        weight_calc = 10 * (est_weight/2.2)
        total_calories_eaten = i[1]
        height_calc = i[2]
        age_calc = i[3]
        sex_calc = i[4]
        act_level = i[5]
        resting_rate = ( (weight_calc+height_calc-age_calc) + sex_calc) * act_level
        day = i[6]


        total_rmr += resting_rate

        calorie_goal = max(resting_rate - i[7], i[8])
        total_calorie_goal += calorie_goal

        log = {
            "date": i[0],
            "profile_id":profile_id,
            'day':day,
            'week':(day//7)+1,
            'est_weight':round(est_weight,1),
            'resting_rate':round(resting_rate,0),
            'eaten_calories':round(total_calories_eaten - previous_total_eaten,0),
            'calorie_goal': round(calorie_goal,0),
            'total_lbs_lost':round((total_rmr - total_calories_eaten)/3500,2),
            'calorie_surplus': round(total_calorie_goal - total_calories_eaten,0),
            'calories_left':round(calorie_goal - (total_calories_eaten-previous_total_eaten),0),
            'bmi':round((est_weight/i[9])*703,2),
            'actual_weight': i[10] or 0
        }
        

        previous_total_eaten = total_calories_eaten
        logs.append(log)
        est_weight = profile.start_weight-((total_rmr - total_calories_eaten)/3500)
    logs.reverse()

    return logs

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
async def get_all_daily(*, profile: Annotated_Profile, db: Session = Depends(deps.get_db)):
    return await daily_log(profile=profile, db=db)
    

    
@router.get(
    "/{current_date}",
    response_model=schemas.DailyOverview,
    status_code=status.HTTP_200_OK,
)
async def get_daily(*, profile: Annotated_Profile, current_date:date, db: Session = Depends(deps.get_db)):
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
    profile_id = profile.id
    weight_data = await get_weight(profile_id=profile_id, current_date=current_date, db=db)
    if weight_data is None:
        output_data = post_daily(actual_weight=daily_data, profile=profile, db=db)
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

