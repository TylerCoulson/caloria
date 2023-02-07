from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship

from app.db import Base

class ServingSize(Base):
    __tablename__ = "serving_size"

    id = Column(Integer, primary_key=True, index=True)
    food_id = Column(Integer, ForeignKey("food.id", ondelete="CASCADE"), nullable=False)
    description = Column(String)
    calories = Column(Integer)
    fats = Column(Integer)
    carbs = Column(Integer)
    protein = Column(Integer)

    food = relationship("Food", back_populates="servings")
