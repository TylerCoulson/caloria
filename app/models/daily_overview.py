from sqlalchemy import Column, ForeignKey, Integer, Date, Float
from sqlalchemy.orm import relationship

from app.db import Base

class DailyLog(Base):
    __tablename__ = "daily_overview"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user.id", ondelete="CASCADE"), nullable=False)
    date = Column(Date)
    actual_weight = Column(Float)
    

    user = relationship('User')