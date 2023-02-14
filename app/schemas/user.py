from pydantic import BaseModel, validator
from datetime import date
from typing import List


class UserBase(BaseModel):
    start_date: date
    email: str
    password_hash: str
    start_weight: float
    end_weight: float
    sex: str
    birthdate: date
    height: int
    lbs_to_lost: float
    activity_level: float

    # @validator("start_weight", "end_weight")
    # def check_start_weight_less_than_end_weight(cls, values):
    #     if values['start_weight'] <= values['end_weight']:
    #         raise ValueError("Start Weight is less than or equal to the end weight")
    #     return values


class UserCreate(UserBase):
    pass

class User(UserBase):
    id: int
    class Config:
        orm_mode = True

class UserLogs(User):
    log: "List[FoodLog]"
    class Config:
        orm_mode = True

from .food_log import FoodLog
UserLogs.update_forward_refs()