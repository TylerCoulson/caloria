from typing import Any
from fastapi.encoders import jsonable_encoder


def create(*, obj_in, db, model) -> Any:
    created = model(**obj_in.dict())
    db.add(created)
    db.commit()
    db.refresh(created)
    return created


def read(*, _id: int, db, model):
    data = db.query(model).filter(model.id == _id).first()
    return data


def update(*, db_obj, data_in, db):
    obj_data = jsonable_encoder(db_obj)

    if isinstance(data_in, dict):
        update_data = data_in
    else:
        update_data = data_in.dict(exclude_unset=True)
    for field in obj_data:
        if field in update_data:
            setattr(db_obj, field, update_data[field])

    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj


def delete(*, _id: int, db, db_obj):
    db.delete(db_obj)
    db.commit()
    return db_obj
