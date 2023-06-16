from sqlalchemy import Column, String, Integer

from app.db import Base

class FoodCategories(Base):
    __tablename__ = "food_categories"

    id = Column(Integer, primary_key=True, index=True)
    description = Column(String)