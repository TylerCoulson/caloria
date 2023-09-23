from pydantic import ConfigDict, BaseModel
from datetime import date

class RecipeCreate(BaseModel):
    finished_food: int
    ingredient: int
    model_config = ConfigDict(from_attributes=True)