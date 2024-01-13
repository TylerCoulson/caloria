from typing import Any
from sqlalchemy import select, or_, and_, false, true, update as sql_update
from sqlalchemy.orm.exc import UnmappedInstanceError
from app import schemas, models


def gatekeeper(data, model, profile):
    non_profile_id_models = [models.Profile, models.ServingSize]
    if not data:
        return None
    if model != models.Profile and model != models.ServingSize:
        if not hasattr(model, "profile_id"):
            return None
        if profile.id != data.profile_id:
            return None 
    if model == models.Profile:
        if profile.id != data.id:
            return None
    if model == models.ServingSize:
        if profile.id != data.food.profile_id:
            return None
    return True
    


async def create(*, obj_in, db, model, profile=None) -> Any:
    if hasattr(model, "profile_id"):
        obj_in.profile_id = profile.id
    
    created = model(**obj_in.model_dump())
    db.add(created)
    await db.commit()
    await db.refresh(created)
    return created


async def read(*, _id: int, db, model, profile:schemas.Profile=None):
    and_criteria = and_(model.id == _id)
    or_criteria = or_(false())

    if hasattr(model, "profile_id"):
        or_criteria = or_(or_criteria, model.profile_id == None)

    if profile and hasattr(model, "profile_id"):
        or_criteria = or_(or_criteria, model.profile_id == profile.id)
    
    if model == models.Profile:
        if profile:
            or_criteria = or_(model.id == profile.id)

    if model == models.ServingSize:
        or_criteria = or_(true())

    criteria = and_(and_criteria, or_criteria)

    statement = select(model).where(criteria)
    data = await db.execute(statement)
    return  data.unique().scalar_one_or_none()

async def read_all_statement(*, n:int=25, page:int=1, db, model, profile:schemas.Profile=None):
    if n < 0:
        n = 25

    offset = max((page-1) * n, 0)

    or_criteria = or_(false())

    if hasattr(model, "profile_id"):
        or_criteria = or_(or_criteria, model.profile_id == None)

    if profile and hasattr(model, "profile_id"):
        or_criteria = or_(or_criteria, model.profile_id == profile.id)

    statement = select(model).limit(n).offset(offset)
    
    return statement


async def read_all(*, n:int=25, page:int=1, db, model, profile:schemas.Profile=None):
    statement = read_all_statement(n=n, page=page, db=db, model=model, profile=profile)
    data = await db.execute(statement)
    return [value for value, in data.unique().all()]

async def update(*, _id, model, update_data, db, profile):
    data = await read(_id=_id, db=db, model=model, profile=profile)

    if gatekeeper(data=data, model=model, profile=profile) is None:
        return None

    try:
        statement = sql_update(model).where(model.id == _id).values(update_data.model_dump())
        await db.execute(statement)
        await db.commit()
        data = await read(_id=_id, db=db, model=model, profile=profile)
        await db.refresh(data)
        return data
    except UnmappedInstanceError:
        return None

async def delete(*, _id: int, db, model, profile):
    data = await read(_id=_id, db=db, model=model, profile=profile)
    if gatekeeper(data=data, model=model, profile=profile) is None:
        return None

    await db.delete(data)
    await db.commit()
    return data
