from pydantic import ConfigDict, BaseModel
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
    model_config = ConfigDict(from_attributes=True)

class ServingSizeNoFood(ServingSizeBase):
    id:int
    model_config = ConfigDict(from_attributes=True)

class AllServings(BaseModel):
    servings: List[ServingSizeNoFood] = []
    model_config = ConfigDict(from_attributes=True)

from .food import FoodNoIngredients
ServingSize.model_rebuild()