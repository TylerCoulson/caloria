from pydantic import BaseModel
from datetime import date
from typing import List
from .food import FoodNoIngredients

class FoodLogBase(BaseModel):
    date: date
    food_id: int
    serving_size_id: int
    serving_amount: int
    profile_id: int

class FoodLogCreate(FoodLogBase):
    pass

class FoodLog(FoodLogBase):
    id: int
    serving_size: "ServingSize"
    class Config:
        orm_mode = True

class FoodLogProfile(FoodLog):
    profile: "Profile"
    class Config:
        orm_mode = True


class DayLog(BaseModel):
    profile: "Profile"
    log: List[FoodLog] = []

    class Config:
        orm_mode = True

from .profile import Profile
from .serving_size import ServingSize
FoodLog.update_forward_refs()
FoodLogProfile.update_forward_refs()
DayLog.update_forward_refs()