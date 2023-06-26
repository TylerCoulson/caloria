from pydantic import BaseModel
from typing import List
from .food_categories import FoodCategory

class FoodBase(BaseModel):
    category_id: int
    type: str
    subtype: str | None

class FoodCreate(FoodBase):
    class Config:
        orm_mode = True

class Food(FoodBase):
    id: int
    # category: FoodCategory
    # ingredients: List["Food"] | None = []
    # servings: List["Food"] | None = []
    class Config:
        orm_mode = True

class FoodNoIngredients(FoodBase):
    id: int
    class Config:
        orm_mode = True

class FoodWithServings(Food):
    servings: List["Food"] | None = []
    class Config:
        orm_mode = True