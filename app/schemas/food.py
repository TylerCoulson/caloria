from pydantic import BaseModel


class FoodBase(BaseModel):
    brand: str
    name: str

class FoodCreate(FoodBase):
    pass

class Food(FoodBase):
    id: int

    class Config:
        orm_mode = True
