from sqlalchemy import Column, ForeignKey, Integer, Date, String, Float
from sqlalchemy.orm import relationship

from app.db import Base

class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True)
    start_date = Column(Date)
    email = Column(String)
    password_hash = Column(String)
    start_weight = Column(Float)
    end_weight = Column(Float)
    sex = Column(String)
    birthdate = Column(Date)
    height = Column(Integer)
    lbs_to_lost = Column(Float)
    activity_level = Column(Float)

    log = relationship('Food_Log', back_populates="user")