from sqlalchemy import Column, ForeignKey, Integer, Date, String, Float
from sqlalchemy.orm import relationship

from app.db import Base

class Profile(Base):
    __tablename__ = "profile"

    id = Column(Integer, primary_key=True, index=True)
    start_date = Column(Date)
    email = Column(String)
    password_hash = Column(String)
    start_weight = Column(Float)
    goal_weight = Column(Float)
    sex = Column(String)
    birthdate = Column(Date)
    height = Column(Integer)
    lbs_per_week = Column(Float)
    activity_level = Column(Float)

    log = relationship('Food_Log', back_populates="profile")