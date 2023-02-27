from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session  # type: ignore
from datetime import date, timedelta
from app import deps
from app import schemas
from app import models
from app import crud

from app.api.calcs.calorie_calcs import PersonsDay 

router = APIRouter()




def daily_log(user_id:int, current_date:date, db):
    output_data = {"date": current_date, "user_id":user_id}
    user_data = crud.read(_id=user_id, db=db, model=models.User)

    log_data = PersonsDay(height=user_data.height, start_weight=user_data.start_weight, start_date=user_data.start_date, lbs_per_day=(user_data.lbs_per_week/7), birthdate=user_data.birthdate, sex=user_data.sex, activity_level=user_data.activity_level, goal_weight=user_data.goal_weight, user_logs=user_data.log) 

    user_age = log_data.age(current_date)
    
    # day
    day = (current_date - user_data.start_date).days
    output_data['day'] = day
    
    # week
    output_data['week'] = (day//7)+1
    
    # estimated_weight
    est_weight = log_data.estimated_weight(current_date=current_date)
    output_data['est_weight'] = est_weight
    
    # resting_rate
    current_rmr  = log_data.resting_rate(weight=est_weight, age=user_age)
    output_data['resting_rate'] = current_rmr
    
    
    # calories_eaten
    calories_eaten_on_current_date = log_data.calories_eaten_today()
    output_data['eaten_calories'] = calories_eaten_on_current_date
    
    # calories goal
    calorie_goal = log_data.calorie_goal(weight=est_weight, age=log_data.age(current_date))
    output_data['calorie_goal'] = calorie_goal
    
    # total_lbs_lost
    total_lbs_lost = log_data.total_lbs_lost(current_date=current_date)
    output_data['total_lbs_lost'] = total_lbs_lost
    
    # calorie surplus
    total_calorie_surplus = log_data.calorie_surplus(current_date=current_date)
    output_data['calorie_surplus'] = total_calorie_surplus

    output_data['calories_left'] = calorie_goal - calories_eaten_on_current_date

    # bmi
    output_data['bmi'] = log_data.bmi(current_date=current_date)

    # actual_weight
    weight_data = db.query(models.DailyLog).filter((models.DailyLog.user_id == user_id) & (models.DailyLog.date == current_date)).first()
    output_data['actual_weight'] = weight_data.actual_weight if weight_data else 0

    return output_data

@router.post(
    "",
    response_model=schemas.DailyOverview,
    status_code=status.HTTP_201_CREATED,
)
def post_daily(*, actual_weight: schemas.DailyOverviewInput, db: Session = Depends(deps.get_db)):
    
    log = crud.create(obj_in=actual_weight, db=db, model=models.DailyLog)
    
    output_data = daily_log(user_id=log.user_id, current_date=log.date, db=db)
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
        output_data.append(daily_log(user_id=user_id, current_date=i_date, db=db))
    
    return output_data

@router.get(
    "/{user_id}/{current_date}",
    response_model=schemas.DailyOverview,
    status_code=status.HTTP_200_OK,
)
def get_daily(*, user_id:int, current_date:date, db: Session = Depends(deps.get_db)):
    output_data = daily_log(user_id=user_id, current_date=current_date, db=db)
    return output_data

@router.put(
    "/{user_id}/{current_date}",
    response_model=schemas.DailyOverview,
    status_code=status.HTTP_200_OK,
)
def update_daily(
    *, user_id:int, current_date:date, daily_data:schemas.DailyOverviewInput, db: Session = Depends(deps.get_db)
):
    
    weight_data = db.query(models.DailyLog).filter((models.DailyLog.user_id == user_id) & (models.DailyLog.date == current_date)).first()
    # data = get_daily(user_id=user_id, current_date=current_date, db=db)
    # 

    data = crud.update(db_obj=weight_data, data_in=daily_data, db=db)
    
    output = daily_log(user_id, current_date, db)

    return output


@router.delete(
    "/{user_id}/{current_date}",
    status_code=status.HTTP_200_OK,
)
def delete_food(*, user_id:int, current_date:date, db: Session = Depends(deps.get_db)):
    weight_data = db.query(models.DailyLog).filter((models.DailyLog.user_id == user_id) & (models.DailyLog.date == current_date)).first()

    data = crud.delete(_id=weight_data.id, db=db, db_obj=weight_data)
    return
