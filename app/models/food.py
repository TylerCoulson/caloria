from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship

from app.db import Base

class Food(Base):
    __tablename__ = "food"

    id = Column(Integer, primary_key=True, index=True)
    brand = Column(String)
    name = Column(String)