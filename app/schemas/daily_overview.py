from pydantic import ConfigDict, BaseModel
from datetime import date


class ActualWeight(BaseModel):
    actual_weight: float | None = 0

class ActivityLevel(BaseModel):
    activity_level: float | None = None

class DailyOptions(ActualWeight, ActivityLevel):
    pass

class DailyOverviewInput(DailyOptions):
    profile_id: int = 0
    date: date

class DailyOverview(DailyOverviewInput):
    day: int
    week: int
    est_weight: float
    calories_burned: int
    eaten_calories: int | None = 0
    eaten_fats: int | None = 0
    eaten_carbs: int | None = 0
    eaten_protein: int | None = 0
    calories_left: int
    calorie_goal: int
    total_lbs_lost: float
    calorie_surplus: int
    bmi: float
    model_config = ConfigDict(from_attributes=True)

