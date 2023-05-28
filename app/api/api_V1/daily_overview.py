from fastapi import APIRouter, Depends, status
from sqlalchemy import select, func, extract, cast, Integer, Numeric, or_, column, Date, Interval, Text
from sqlalchemy.orm import Session  # type: ignore
from datetime import date
from app import deps
from app import schemas
from app import models
from app import crud

from app.api.calcs.calorie_calcs import PersonsDay 
from app.auth.router import Annotated_Profile
router = APIRouter()


async def get_weight(profile_id, current_date, db: Session):
    statement = select(models.DailyLog).where(models.DailyLog.profile_id == profile_id).where(models.DailyLog.date == current_date)
    data = await db.execute(statement)
    return data.unique().scalar_one_or_none()

async def daily_log(profile:models.Profile, db: Session):

    if profile is None:
        raise ValueError("profile cannot be None")

    date_range = func.generate_series(cast(profile.start_date, Date), cast(date.today(), Date), cast(cast('1 day', Text), Interval)).alias('dates')
    dates = column("dates")

    statement = select(
        cast(dates, Date),
        func.sum(models.ServingSize.calories * models.Food_Log.serving_amount).over(order_by=dates), # total_calories_eaten
        (profile.height*2.54) * 6.25, #height
        cast((extract('epoch', dates) - extract('epoch', profile.birthdate))/60/60/24/365.25, Integer) * 5, #age
        -161 if profile.sex == 'female' else 5, #sex
        profile.activity_level, #activity level
        cast((extract('epoch', dates) - extract('epoch', profile.start_date))/60/60/24, Integer)+1, # days since start
        profile.lbs_per_week * 500, # calories need to lose per week
        1200 if profile.sex == 'female' else 1500, # lowest calories allowed
        profile.height * profile.height, # heigh squared (used for bmi calc)
        models.DailyLog.actual_weight # user inputed weight
    ).select_from(date_range).join(models.Food_Log, models.Food_Log.date == dates, isouter=True                                           
    ).where(or_(models.Food_Log.profile_id == 1, models.Food_Log.profile_id == None)
    ).join(models.ServingSize, isouter=True
    ).join(models.DailyLog, models.DailyLog.date == models.Food_Log.date, isouter=True
    )
    
    data = await db.execute(statement)
    logs = []

    total_rmr = 0
    est_weight = profile.start_weight
    total_calorie_goal = 0
    previous_total_eaten = 0
    
    for i in data.unique().all():
        weight_calc = 10 * (est_weight/2.2)
        total_calories_eaten = float(i[1])
        height_calc = float(i[2])
        age_calc = float(i[3])
        sex_calc = float(i[4])
        act_level = float(i[5])
        resting_rate = ( (weight_calc+height_calc-age_calc) + sex_calc) * act_level
        day = i[6]


        total_rmr += resting_rate

        calorie_goal = max(resting_rate - float(i[7]), float(i[8]))
        total_calorie_goal += calorie_goal

        log = {
            "date": i[0],
            "profile_id":profile.id,
            'day':day,
            'week':(day//7)+1,
            'est_weight':round(est_weight,1),
            'resting_rate':round(resting_rate,0),
            'eaten_calories':round(total_calories_eaten - previous_total_eaten,0),
            'calorie_goal': round(calorie_goal,0),
            'total_lbs_lost':round((total_rmr - total_calories_eaten)/3500,2),
            'calorie_surplus': round(total_calorie_goal - total_calories_eaten,0),
            'calories_left':round(calorie_goal - (total_calories_eaten-previous_total_eaten),0),
            'bmi':round((est_weight/float(i[9]))*703,2),
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

