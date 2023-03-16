from pydantic import BaseModel, validator
from datetime import date
from typing import List

class ProfileBase(BaseModel):
    start_date: date
    start_weight: float
    goal_weight: float
    sex: str
    birthdate: date
    height: int
    lbs_per_week: float
    activity_level: float
    
    # @validator("start_weight", "goal_weight")
    # def check_start_weight_less_than_goal_weight(cls, values):
    #     if values['start_weight'] <= values['goal_weight']:
    #         raise ValueError("Start Weight is less than or equal to the end weight")
    #     return values


class ProfileCreate(ProfileBase):
    user_id: int
    pass

class Profile(ProfileCreate):
    id: int
    class Config:
        orm_mode = True

class ProfileLogs(Profile):
    log: "List[FoodLog]"
    class Config:
        orm_mode = True

from .food_log import FoodLog
ProfileLogs.update_forward_refs()