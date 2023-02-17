from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session  # type: ignore
from datetime import date, timedelta
from app import deps
from app import schemas
from app import models
from app import crud

from app.api.calcs import calorie_calcs

router = APIRouter()




def daily_log(user_id:int, date:date, db):
    output_data = {"date": date, "user_id":user_id}
    user_data = crud.read(_id=user_id, db=db, model=models.User)

    user_age = calorie_calcs.age(user_data.birthdate, date)
    start_rmr = calorie_calcs.resting_rate(weight=user_data.start_weight, height=user_data.height, age=user_age, sex=user_data.sex, activity_level=user_data.activity_level)
    
    # days
    days = calorie_calcs.days_between(start_date=user_data.start_date, end_date=date)
    output_data['day'] = days
    
    # week
    output_data['week'] = (days//7)+1
    
    # total_calories_eaten
    total_calories_eaten = calorie_calcs.total_calories_eaten(logs=user_data.log, date=date, start_date=user_data.start_date)
    
    # estimated_weight
    est_weight = calorie_calcs.estimated_weight(
        total_calories_eaten=total_calories_eaten,
        start_weight=user_data.start_weight,
        lbs_per_day=user_data.lbs_to_lost/7,
        days=days,
        start_age=calorie_calcs.age(user_data.birthdate, user_data.start_date),
        current_age=user_age,
        height=user_data.height,
        sex=user_data.sex,
        activity_level=user_data.activity_level)
    output_data['est_weight'] = est_weight
    
    # resting_rate
    current_rmr  = calorie_calcs.resting_rate(est_weight, user_data.height, user_age, user_data.sex, user_data.activity_level)
    output_data['resting_rate'] = current_rmr
    
    
    # calories_eaten
    calories_eaten_on_current_date = calorie_calcs.calories_eaten(user_data.log, date)
    output_data['eaten_calories'] = calories_eaten_on_current_date
    
    # calories goal
    calorie_goal = calorie_calcs.calorie_goal(est_weight, user_data.end_weight, current_rmr, user_data.lbs_to_lost, user_data.sex)
    output_data['calorie_goal'] = calorie_goal
    
    # total_lbs_lost
    total_lbs_lost = calorie_calcs.total_lbs_lost(user_data.start_weight, est_weight)
    output_data['total_lbs_lost'] = total_lbs_lost
    
    # calorie surplus
    total_calorie_surplus = calorie_calcs.calorie_surplus(
        start_weight=user_data.start_weight, 
        est_weight=est_weight, 
        cals_eatten=total_calories_eaten, 
        start_rmr=start_rmr, 
        est_rmr=current_rmr, 
        goal_weight=user_data.end_weight, 
        days=days, 
        weekly_lbs_lose=user_data.lbs_to_lost, 
        sex=user_data.sex
    )
    output_data['calorie_surplus'] = total_calorie_surplus

    output_data['date'] = date
    output_data['calories_left'] = calorie_goal - calories_eaten_on_current_date

    # bmi
    output_data['bmi'] = calorie_calcs.bmi(user_data.height, est_weight)

    # actual_weight
    weight_data = db.query(models.DailyLog).filter((models.DailyLog.user_id == user_id) & (models.DailyLog.date == date)).first()
    output_data['actual_weight'] = weight_data.actual_weight if weight_data else 0

    return output_data

@router.post(
    "",
    response_model=schemas.DailyOverview,
    status_code=status.HTTP_201_CREATED,
)
def post_daily(*, actual_weight: schemas.DailyOverviewInput, db: Session = Depends(deps.get_db)):
    
    log = crud.create(obj_in=actual_weight, db=db, model=models.DailyLog)
    
    output_data = daily_log(user_id=log.user_id, date=log.date, db=db)
    return output_data

@router.get(
    "/all",
    response_model=schemas.DailyOverview,
    status_code=status.HTTP_200_OK,
)
def get_all_daily(*, user_id:int, n_days:int=50, db: Session = Depends(deps.get_db)):
    user_data = crud.read(_id=user_id, db=db, model=models.User)
    output_data = []
    current_date = date.today()
    start_date = user_data.start_date
    total_days = (current_date - start_date).days
    for i in range(min(total_days, n_days)+1):
        i_date = current_date - timedelta(i)
        output_data.append(daily_log(user_id=user_id, date=i_date, db=db))
    
    return output_data

@router.get(
    "/{user_id}/{date}",
    response_model=schemas.DailyOverview,
    status_code=status.HTTP_200_OK,
)
def get_daily(*, user_id:int, date:date, db: Session = Depends(deps.get_db)):
    output_data = daily_log(user_id=user_id, date=date, db=db)
    
    return output_data