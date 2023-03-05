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
    "/1/{profile_id}",
    response_model=Dict[int, schemas.Prediction],
    status_code=status.HTTP_200_OK,
)
def get_predictions_never_fault(*, profile_id:int, db: Session = Depends(deps.get_db)):
    profile_data = crud.read(_id=profile_id, db=db, model=models.Profile)
    log_data = PersonsDay(height=profile_data.height, start_weight=profile_data.start_weight, start_date=profile_data.start_date, lbs_per_day=(profile_data.lbs_per_week/7), birthdate=profile_data.birthdate, sex=profile_data.sex, activity_level=profile_data.activity_level, goal_weight=profile_data.goal_weight, profile_logs=profile_data.log) 
    pred = log_data.prediction()    
    return pred


@router.get(
    "/2/{profile_id}",
    response_model=Dict[int, schemas.Prediction],
    status_code=status.HTTP_200_OK,
)
def get_predictions_updates_lbs_to_lose(*, profile_id:int, current_date:date, db: Session = Depends(deps.get_db)):
    profile_data = crud.read(_id=profile_id, db=db, model=models.Profile)    
    log_data = PersonsDay(height=profile_data.height, start_weight=profile_data.start_weight, start_date=profile_data.start_date, lbs_per_day=(profile_data.lbs_per_week/7), birthdate=profile_data.birthdate, sex=profile_data.sex, activity_level=profile_data.activity_level, goal_weight=profile_data.goal_weight, profile_logs=profile_data.log) 
    
    total_days = (current_date - profile_data.start_date).days
    
    if total_days:
        log_data.lbs_per_day = log_data.total_lbs_lost(current_date=current_date) / total_days
    
    pred = log_data.prediction()    
    return pred