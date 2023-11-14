from fastapi import status, HTTPException
from sqlalchemy import select, or_, nulls_last, Select
from sqlalchemy.orm import Session
from app import models, crud
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

async def get_food_by_id(*, deps:CommonDeps, food_id: int):
    user_id = get_user_id(deps=deps)
    data = await crud.read(_id=food_id, db=deps['db'], model=models.Food)
    
    if not data or (user_id != data.user_id and data.user_id is not None):
        raise HTTPException(status_code=404, detail="Food not found")
    return data

async def check_food_authorized(deps:CommonDeps, food_id:int):
    food = await get_food_by_id(deps=deps, food_id=food_id)

    if food.user_id is None:
        return food
    if food.user_id == get_user_id(deps=deps):
        return food

    raise HTTPException(status_code=403, detail="Not Authorized")