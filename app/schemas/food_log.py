from pydantic import ConfigDict, BaseModel
from datetime import date
from typing import List
from .food import FoodNoIngredients

class FoodLogBase(BaseModel):
    date: date
    food_id: int
    serving_size_id: int
    serving_amount: float
    profile_id: int = 0

class FoodLogCreate(FoodLogBase):
    pass

class FoodLog(FoodLogBase):
    id: int
    serving_size: "ServingSize"
    model_config = ConfigDict(from_attributes=True)

class FoodLogProfile(FoodLog):
    profile: "Profile"
    model_config = ConfigDict(from_attributes=True)


class DayLog(BaseModel):
    profile: "Profile"
    log: List[FoodLog] = []
    model_config = ConfigDict(from_attributes=True)

from .profile import Profile
from .serving_size import ServingSize
FoodLog.model_rebuild()
FoodLogProfile.model_rebuild()
DayLog.model_rebuild()