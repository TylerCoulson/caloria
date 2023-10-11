from pydantic import ConfigDict, BaseModel
from typing import List
from .food_categories import FoodCategory

class FoodBase(BaseModel):
    user_id: int | None = None
    category_id: int
    type: str
    subtype: str | None = None

class FoodCreate(FoodBase):
    model_config = ConfigDict(from_attributes=True)

class Food(FoodBase):
    id: int
    category: FoodCategory
    model_config = ConfigDict(from_attributes=True)

class FoodNoIngredients(FoodBase):
    id: int
    model_config = ConfigDict(from_attributes=True)

class FoodWithServings(Food):
    servings: List["Food"] | None = []
    model_config = ConfigDict(from_attributes=True)