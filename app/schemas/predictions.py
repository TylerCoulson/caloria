from pydantic import BaseModel
from datetime import date

class Prediction(BaseModel):
    day: int 
    week: int
    date: date 
    est_weight: float 
    resting_rate: int 
    net_calories: int 
    total_lbs_lost: float 
    lbs_lost_today: float
    bmi: float
