from pydantic import BaseModel
from datetime import date


class DailyOutputBase(BaseModel):
    day: int
    week: int
    date: date
    actual_weight: float | None = 0
    est_weight: float
    resting_rate: int
    eaten_calories: int | None = 0
    calories_left: int
    calorie_goal: int

    total_lbs_lost: float
    calorie_surplus: int
    user_id: int


class DailyOutputInput(BaseModel):
    user_id: int
    date: date