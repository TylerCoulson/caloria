from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session  # type: ignore
from datetime import date, timedelta, datetime
from typing import Dict
from app import deps
from app import schemas
from app import models
from app import crud

from app.api.calcs.calorie_calcs import PersonsDay 

router = APIRouter()


async def weight_params(height:int, start_weight:float, start_date:date, lbs_per_week:float, birthdate:date, sex:str, activity_level:float, goal_weight:float, log:list=[]):
    return {'height':height, 'start_weight':start_weight, 'start_date':start_date, 'lbs_per_week':lbs_per_week, 'birthdate':birthdate, 'sex':sex, 'activity_level':activity_level, 'goal_weight':goal_weight, 'log':log,}

@router.get(
    "/never_faulter",
    response_model=Dict[int, schemas.Prediction],
    status_code=status.HTTP_200_OK,
)
async def get_predictions_never_fault(*, params: dict=Depends(weight_params), db: Session = Depends(deps.get_db)):
    print("tests")
    log_data = PersonsDay(height=params['height'], start_weight=params['start_weight'], start_date=params['start_date'], lbs_per_day=params['lbs_per_week']/7, birthdate=params['birthdate'], sex=params['sex'], activity_level=params['activity_level'], goal_weight=params['goal_weight'], profile_logs=params['log']) 
    pred = log_data.prediction()    
    return pred


@router.get(
    "/update_lbs_to_lose",
    response_model=Dict[int, schemas.Prediction],
    status_code=status.HTTP_200_OK,
)
async def get_predictions_updates_lbs_to_lose(*, params: dict=Depends(weight_params), current_date:date = None, db: Session = Depends(deps.get_db)):
    
    if current_date is None:
        current_date = params['start_date']
    log_data = PersonsDay(height=params['height'], start_weight=params['start_weight'], start_date=params['start_date'], lbs_per_day=params['lbs_per_week']/7, birthdate=params['birthdate'], sex=params['sex'], activity_level=params['activity_level'], goal_weight=params['goal_weight'], profile_logs=params['log']) 
    total_days = (current_date - params['start_date']).days
    
    if total_days:
        log_data.lbs_per_day = log_data.total_lbs_lost(current_date=current_date) / total_days
    
    pred = log_data.prediction()    
    return pred