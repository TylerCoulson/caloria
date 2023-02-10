from pydantic import BaseModel
from typing import List

class FoodBase(BaseModel):
    brand: str
    name: str

class FoodCreate(FoodBase):
    pass

class Food(FoodBase):
    id: int
    ingredients: List["Food"] | None = []
    # servings: List["Food"] | None = []
    class Config:
        orm_mode = True

class FoodWithServings(Food):
    servings: List["Food"] | None = []
    class Config:
        orm_mode = True