from pydantic import BaseModel
from datetime import date
from typing import List
from .food import Food
from .serving_size import ServingSize

class FoodLogBase(BaseModel):
    date: date
    food_id: int
    serving_size_id: int
    serving_amount: int
    user_id: int

class FoodLogCreate(FoodLogBase):
    pass

class FoodLog(FoodLogBase):
    id: int
    food: Food
    serving_size: ServingSize
    class Config:
        orm_mode = True

class FoodLogUser(FoodLog):
    user: "User"
    class Config:
        orm_mode = True

class DayLog(BaseModel):
    user: "User"
    log: List[FoodLog] = []

    class Config:
        orm_mode = True

from .user import User
FoodLogUser.update_forward_refs()
DayLog.update_forward_refs()