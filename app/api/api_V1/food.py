from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session  # type: ignore
from typing import List, Tuple
from fastapi.encoders import jsonable_encoder
from sqlalchemy import select
from app import deps
from app import schemas
from app import models

router = APIRouter(tags=["food"])

from app import crud


@router.post(
    "",
    response_model=schemas.Food,
    status_code=status.HTTP_201_CREATED,
)
async def post_food(*, food: schemas.FoodCreate, db: Session = Depends(deps.get_db)):
    food_out = await crud.create(obj_in=food, db=db, model=models.Food)
    return food_out

@router.get(
    "/search",
    response_model=List[schemas.Food],
    status_code=status.HTTP_200_OK,
)
async def get_food_search(*, search_for:str, search_word:str, n:int=25, db: Session = Depends(deps.get_db)):
    statement = select(models.Food).where(getattr(models.Food, search_for).contains(search_word)).limit(n)
    data = await db.execute(statement)
    all_data = data.unique().all()

    if not all_data:
        raise HTTPException(status_code=404, detail="Food not found")

    return [value for value, in all_data]

@router.get(
    "/all",
    response_model=List[schemas.Food],
    status_code=status.HTTP_200_OK,
)
async def get_all_foods(*, n:int=25, db: Session = Depends(deps.get_db)):
    statement = select(models.Food).limit(n)
    data = await db.execute(statement)
    return [value for value, in data.all()]

@router.get(
    "/{food_id}",
    response_model=schemas.Food,
    status_code=status.HTTP_200_OK,
)
async def get_food_id(*, food_id: int, db: Session = Depends(deps.get_db)):
    data = await crud.read(_id=food_id, db=db, model=models.Food)
    if not data:
        raise HTTPException(status_code=404, detail="Food not found")
    return data

@router.put(
    "/{food_id}",
    response_model=schemas.Food,
    status_code=status.HTTP_200_OK,
)
async def update_food(
    *, food_id: int, food_in: schemas.FoodBase, db: Session = Depends(deps.get_db)
):
    data = await get_food_id(food_id=food_id, db=db)

    data = await crud.update(db_obj=data, data_in=food_in, db=db)

    return data


@router.delete(
    "/{food_id}",
    status_code=status.HTTP_200_OK,
)
async def delete_food(*, food_id: int, db: Session = Depends(deps.get_db)):
    data = await get_food_id(food_id=food_id, db=db)

    data = await crud.delete(_id=food_id, db=db, db_obj=data)
    return
