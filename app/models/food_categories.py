from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship
from app.db import Base

class FoodCategories(Base):
    __tablename__ = "food_categories"

    id = Column(Integer, primary_key=True, index=True)
    description = Column(String)

    food = relationship(
        "Food", back_populates="category", lazy="joined", cascade="all, delete-orphan"
    )