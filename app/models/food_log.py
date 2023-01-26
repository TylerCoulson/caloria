from sqlalchemy import Column, ForeignKey, Integer, Date, DECIMAL
from sqlalchemy.orm import relationship

from app.db import Base

class Food_Log(Base):
    __tablename__ = "food_log"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date)
    food_id = Column(Integer, ForeignKey("food.id", ondelete="CASCADE"), nullable=False)
    serving_size_id = Column(Integer, ForeignKey("serving_size.id", ondelete="CASCADE"), nullable=False)
    serving_amount = Column(Integer)
    user_id = Column(Integer, ForeignKey("user.id", ondelete="CASCADE"), nullable=False)

    food = relationship("Food")
    serving_size = relationship("ServingSize")
    user = relationship('User', back_populates="log")