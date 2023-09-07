from pydantic import BaseModel


class FoodCategoryCreate(BaseModel):
    description: str

class FoodCategory(FoodCategoryCreate):
    id: int

    class Config:
        orm_mode = True