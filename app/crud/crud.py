from typing import Any
from sqlalchemy import select, update as sql_update
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.encoders import jsonable_encoder


async def create(*, obj_in, db, model) -> Any:
    created = model(**obj_in.dict())
    db.add(created)
    await db.commit()
    await db.refresh(created)
    return created


async def read(*, _id: int, db, model):
    statement = select(model).where(model.id == _id)
    data = await db.execute(statement)
    return  data.unique().scalar_one_or_none()


async def update(*, _id, model, update_data, db):
    statement = sql_update(model).where(model.id == _id).values(update_data.dict())
    await db.execute(statement)
    
    await db.commit()
    data = await read(_id=_id, db=db, model=model)
    await db.refresh(data)
    return data


async def delete(*, _id: int, db, db_obj):
    await db.delete(db_obj)
    await db.commit()
    return db_obj
