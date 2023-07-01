from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session  # type: ignore
from typing import List, Tuple
from fastapi.encoders import jsonable_encoder
from sqlalchemy import select, func
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
async def get_food_search(*, search_word:str, n:int=25, page:int=1, db: Session = Depends(deps.get_db)):
    offset = max((page-1) * n, 0)

    statement = select(models.Food).where(
        func.lower(models.Food.type).contains(search_word) | func.lower(models.Food.subtype).contains(search_word) 
    ).limit(n
    ).offset(offset)
    
    data = await db.execute(statement)
    
    all_data = data.unique().all()

    return [value for value, in all_data]

@router.get(
    "/all",
    response_model=List[schemas.Food],
    status_code=status.HTTP_200_OK,
)
async def get_all_foods(*, n:int=25, page:int=1, db: Session = Depends(deps.get_db)):
    return await crud.read_all(n=n, page=page, db=db, model=models.Food)

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
    data = await crud.update(_id=food_id, model=models.Food, update_data=food_in, db=db)
    
    if data is None:
        raise HTTPException(status_code=404, detail="No food with this id")
    return data


@router.delete(
    "/{food_id}",
    status_code=status.HTTP_200_OK,
)
async def delete_food(*, food_id: int, db: Session = Depends(deps.get_db)):
    data = await get_food_id(food_id=food_id, db=db)

    data = await crud.delete(_id=food_id, db=db, db_obj=data)
    return
