# from typing import Annotated
# from fastapi import APIRouter, Depends, status, HTTPException
# from datetime import date
# from typing import Dict
# from app import schemas

# from app.api.calcs.calorie_calcs import PersonsDay 

# router = APIRouter()


# async def weight_params(height:int, start_weight:float, start_date:date, lbs_per_week:float, birthdate:date, sex:str, activity_level:float, goal_weight:float, log:list=[]):
#     return {'height':height, 'start_weight':start_weight, 'start_date':start_date, 'lbs_per_week':lbs_per_week, 'birthdate':birthdate, 'sex':sex, 'activity_level':activity_level, 'goal_weight':goal_weight, 'log':log,}


# WeightParams = Annotated[dict, Depends(weight_params)]

# @router.get(
#     "/never_faulter",
#     response_model=Dict[int, schemas.Prediction],
#     status_code=status.HTTP_200_OK,
# )
# async def get_predictions_never_fault(*, params:WeightParams):
#     log_data = PersonsDay(height=params['height'], start_weight=params['start_weight'], start_date=params['start_date'], lbs_per_day=params['lbs_per_week']/7, birthdate=params['birthdate'], sex=params['sex'], activity_level=params['activity_level'], goal_weight=params['goal_weight'], profile_logs=params['log']) 
    
#     if isinstance(log_data.check_possible(), str):
#         raise HTTPException(status_code=404, detail=log_data.check_possible())

#     pred = log_data.prediction()    
#     return pred


# @router.get(
#     "/update_lbs_to_lose",
#     response_model=Dict[int, schemas.Prediction],
#     status_code=status.HTTP_200_OK,
# )
# async def get_predictions_updates_lbs_to_lose(*, params:WeightParams, current_date:date = None):
    
#     if current_date is None:
#         current_date = params['start_date']
#     log_data = PersonsDay(height=params['height'], start_weight=params['start_weight'], start_date=params['start_date'], lbs_per_day=params['lbs_per_week']/7, birthdate=params['birthdate'], sex=params['sex'], activity_level=params['activity_level'], goal_weight=params['goal_weight'], profile_logs=params['log']) 
#     total_days = (current_date - params['start_date']).days
    
#     if total_days:
#         log_data.lbs_per_day = log_data.total_lbs_lost(current_date=current_date) / total_days
    
#     pred = log_data.prediction()    
#     return pred