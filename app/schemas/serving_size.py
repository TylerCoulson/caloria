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
    food: "FoodNoIngredients"
    class Config:
        orm_mode = True

class ServingSizeNoFood(ServingSizeBase):
    id:int

class AllServings(BaseModel):
    servings: List[ServingSize] = []

    class Config:
        orm_mode = True

from schemas import FoodNoIngredients
ServingSize.update_forward_refs()