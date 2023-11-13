from sqlalchemy import select, or_, nulls_last, Select
from sqlalchemy.orm import Session
from app import models
from app.api.api_V1.deps import CommonDeps

default_n = 25

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
        n = default_n

    offset = max((page-1) * n, 0)
    return offset

def get_user_id(deps:CommonDeps):
    return None if deps['user'] is None else deps['user'].id

def get_all_statement(deps:CommonDeps, n:int, page:int) -> Select:
    n = n if n > 0 else default_n
    offset = get_offset(page=page, n=n)
    user_id = get_user_id(deps=deps)

    statement = select(models.Food
    ).where(or_(models.Food.user_id == user_id, models.Food.user_id == None)
    ).order_by(nulls_last(models.Food.user_id.desc()), models.Food.category_id, models.Food.type, models.Food.subtype
    ).limit(n
    ).offset(offset)

    return statement