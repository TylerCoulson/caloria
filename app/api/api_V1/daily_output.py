from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session  # type: ignore
from datetime import date
from app import deps
from app import schemas
from app import models

from app.api.calcs.calcs import resting_rate, age
from app.api.calcs import calorie_calcs

router = APIRouter()

from app import crud


@router.get(
    "/{user_id}/{date}",
    response_model=schemas.DailyOutputBase,
    status_code=status.HTTP_200_OK,
)
def get_daily(*, user_id:int, date:date, db: Session = Depends(deps.get_db)):
    output_data = {"date": date, "user_id":user_id}
    user_data = crud.read(_id=user_id, db=db, model=models.User)

    user_age = age(user_data.birthdate, date)
    start_rmr = resting_rate(weight=user_data.start_weight, height=user_data.height, age=user_age, sex=user_data.sex, activity_level=user_data.activity_level)
    
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
        start_age=age(user_data.birthdate, user_data.start_date),
        current_age=user_age,
        height=user_data.height,
        sex=user_data.sex,
        activity_level=user_data.activity_level)
    output_data['est_weight'] = est_weight
    
    # resting_rate
    current_rmr  = resting_rate(est_weight, user_data.height, user_age, user_data.sex, user_data.activity_level)
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
    
    return output_data