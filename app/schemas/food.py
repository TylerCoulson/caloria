from pydantic import ConfigDict, BaseModel
from typing import List
from .food_categories import FoodCategory

class FoodNoSubtype(BaseModel):
    category_id: int
    type: str
    
class FoodBase(FoodNoSubtype):
    user_id: int | None = None
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