from pydantic import BaseModel
from datetime import date

class DailyOverviewInput(BaseModel):
    profile_id: int
    date: date
    actual_weight: float | None = 0


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

