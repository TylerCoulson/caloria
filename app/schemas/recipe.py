from pydantic import BaseModel
from datetime import date

class RecipeCreate(BaseModel):
    finished_food: int
    ingredient: int

    class Config:
        orm_mode = True