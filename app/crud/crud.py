from typing import Any
from sqlalchemy import select, update as sql_update
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm.exc import UnmappedInstanceError

async def create(*, obj_in, db, model, profile=None) -> Any:
    if hasattr(model, "profile_id"):
        obj_in.profile_id = profile.id
    
    created = model(**obj_in.model_dump())
    db.add(created)
    await db.commit()
    await db.refresh(created)
    return created


async def read(*, _id: int, db, model):
    statement = select(model).where(model.id == _id)
    data = await db.execute(statement)
    return  data.unique().scalar_one_or_none()

async def read_all(*, n:int=25, page:int=1, db, model):
    if n < 0:
        n = 25

    offset = max((page-1) * n, 0)

    statement = select(model).limit(n).offset(offset)
    data = await db.execute(statement)
    return [value for value, in data.unique().all()]

async def update(*, _id, model, update_data, db, profile=None):
    if hasattr(model, "profile_id"):
        update_data.profile_id = profile.id
    try:
        statement = sql_update(model).where(model.id == _id).values(update_data.model_dump())
        await db.execute(statement)
        await db.commit()
        data = await read(_id=_id, db=db, model=model)
        await db.refresh(data)
        return data
    except UnmappedInstanceError:
        return None



async def delete(*, _id: int, db, db_obj):
    await db.delete(db_obj)
    await db.commit()
    return db_obj
