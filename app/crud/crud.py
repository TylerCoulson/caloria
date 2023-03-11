from typing import Any
from sqlalchemy import select
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


async def update(*, db_obj, data_in, db):
    obj_data = jsonable_encoder(db_obj)

    if isinstance(data_in, dict):
        update_data = data_in
    else:
        update_data = data_in.dict(exclude_unset=True)
    for field in obj_data:
        if field in update_data:
            setattr(db_obj, field, update_data[field])

    db.add(db_obj)
    await db.commit()
    await db.refresh(db_obj)
    return db_obj


async def delete(*, _id: int, db, db_obj):
    await db.delete(db_obj)
    await db.commit()
    return db_obj
