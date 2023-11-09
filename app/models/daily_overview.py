from sqlalchemy import Column, ForeignKey, Integer, Date, Float
from sqlalchemy.orm import relationship

from app.db import Base

class DailyLog(Base):
    __tablename__ = "daily_overview"

    id = Column(Integer, primary_key=True, index=True)
    profile_id = Column(Integer, ForeignKey("profile.id", ondelete="CASCADE"), nullable=False)
    date = Column(Date)
    actual_weight = Column(Float)
    activity_level = Column(Float)
    

    profile = relationship('Profile', lazy='selectin')