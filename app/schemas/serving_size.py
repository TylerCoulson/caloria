from pydantic import BaseModel
from datetime import date
from typing import List

class ServingSizeBase(BaseModel):
    food_id: int
    description: str
    calories: int
    fats: int
    carbs: int
    protein: int

class ServingSizeCreate(ServingSizeBase):
    pass

class ServingSize(ServingSizeBase):
    id: int

    class Config:
        orm_mode = True

class AllServings(BaseModel):
    servings: List[ServingSize] = []

    class Config:
        orm_mode = True