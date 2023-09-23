from pydantic import ConfigDict, BaseModel


class FoodCategoryCreate(BaseModel):
    description: str

class FoodCategory(FoodCategoryCreate):
    id: int
    model_config = ConfigDict(from_attributes=True)