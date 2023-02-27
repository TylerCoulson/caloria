from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session  # type: ignore
from datetime import date, timedelta
from typing import Dict
from app import deps
from app import schemas
from app import models
from app import crud

from app.api.calcs.calorie_calcs import PersonsDay 

router = APIRouter()

@router.get(
    "/1/{user_id}",
    response_model=Dict[int, schemas.Prediction],
    status_code=status.HTTP_200_OK,
)
def get_predictions_never_fault(*, user_id:int, db: Session = Depends(deps.get_db)):
    user_data = crud.read(_id=user_id, db=db, model=models.User)
    log_data = PersonsDay(height=user_data.height, start_weight=user_data.start_weight, start_date=user_data.start_date, lbs_per_day=(user_data.lbs_per_week/7), birthdate=user_data.birthdate, sex=user_data.sex, activity_level=user_data.activity_level, goal_weight=user_data.goal_weight, user_logs=user_data.log) 
    pred = log_data.prediction()    
    return pred


@router.get(
    "/2/{user_id}",
    response_model=Dict[int, schemas.Prediction],
    status_code=status.HTTP_200_OK,
)
def get_predictions_updates_lbs_to_lose(*, user_id:int, current_date:date, db: Session = Depends(deps.get_db)):
    user_data = crud.read(_id=user_id, db=db, model=models.User)    
    log_data = PersonsDay(height=user_data.height, start_weight=user_data.start_weight, start_date=user_data.start_date, lbs_per_day=(user_data.lbs_per_week/7), birthdate=user_data.birthdate, sex=user_data.sex, activity_level=user_data.activity_level, goal_weight=user_data.goal_weight, user_logs=user_data.log) 
    
    total_days = (current_date - user_data.start_date).days
    
    if total_days:
        log_data.lbs_per_day = log_data.total_lbs_lost(current_date=current_date) / total_days

    pred = log_data.prediction()    
    return pred