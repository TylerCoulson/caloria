from sqlalchemy import select
from sqlalchemy.orm import Session
from app import models

async def get_weight(profile_id, current_date, db: Session):
    statement = select(models.DailyLog).where(models.DailyLog.profile_id == profile_id).where(models.DailyLog.date == current_date)
    data = await db.execute(statement)
    return data.unique().scalar_one_or_none()

async def get_day_activity_level(profile_id, current_date, db: Session):
    statement = select(models.DailyLog.activity_level).where(models.DailyLog.profile_id == profile_id).where(models.DailyLog.date == current_date)
    data = await db.execute(statement)
    return data.unique().scalar_one_or_none()

def get_offset(page:int, n:int):
    if n < 0:
        n = 25

    offset = max((page-1) * n, 0)
    return offset

# def get_date_as_date