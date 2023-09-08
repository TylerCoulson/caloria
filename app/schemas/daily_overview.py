from pydantic import BaseModel
from datetime import date


class ActualWeight(BaseModel):
    actual_weight: float | None = 0

class DailyOverviewInput(ActualWeight):
    profile_id: int = 0
    date: date



class DailyOverview(DailyOverviewInput):
    day: int
    week: int
    est_weight: float
    resting_rate: int
    eaten_calories: int | None = 0
    calories_left: int
    calorie_goal: int
    total_lbs_lost: float
    calorie_surplus: int
    bmi: float


    class Config:
        orm_mode = True

