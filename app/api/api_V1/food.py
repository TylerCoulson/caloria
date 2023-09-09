from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session  # type: ignore
from typing import List, Tuple
from fastapi.encoders import jsonable_encoder
from sqlalchemy import select, func
from app import deps
from app import schemas
from app import models
from app.api.api_V1.deps import CommonDeps
from app import crud


router = APIRouter(tags=["food"])



@router.post(
    "",
    response_model=schemas.Food,
    status_code=status.HTTP_201_CREATED,
)
async def post_food(*, deps:CommonDeps, food: schemas.FoodCreate):
    food_out = await crud.create(obj_in=food, db=deps['db'], model=models.Food)
    return food_out

@router.get(
    "/search",
    response_model=List[schemas.Food],
    status_code=status.HTTP_200_OK,
)
async def get_food_search(*, deps:CommonDeps,search_word:str, n:int=25, page:int=1):
    offset = max((page-1) * n, 0)

    statement = select(models.Food).where(
        func.lower(models.Food.type).contains(search_word) | func.lower(models.Food.subtype).contains(search_word) 
    ).limit(n
    ).offset(offset)
    
    data = await deps['db'].execute(statement)
    
    all_data = data.unique().all()

    return [value for value, in all_data]

@router.get(
    "/all",
    response_model=List[schemas.Food],
    status_code=status.HTTP_200_OK,
)
async def get_all_foods(*, deps:CommonDeps, n:int=25, page:int=1):
    return await crud.read_all(n=n, page=page, db=deps['db'], model=models.Food)

@router.get(
    "/{food_id}",
    response_model=schemas.Food,
    status_code=status.HTTP_200_OK,
)
async def get_food_id(*, deps:CommonDeps, food_id: int):
    data = await crud.read(_id=food_id, db=deps['db'], model=models.Food)
    if not data:
        raise HTTPException(status_code=404, detail="Food not found")
    return data

@router.put(
    "/{food_id}",
    response_model=schemas.Food,
    status_code=status.HTTP_200_OK,
)
async def update_food(
    *, deps:CommonDeps, food_id: int, food_in: schemas.FoodBase
):
    data = await crud.update(_id=food_id, model=models.Food, update_data=food_in, db=deps['db'])
    
    if data is None:
        raise HTTPException(status_code=404, detail="No food with this id")
    return data


@router.delete(
    "/{food_id}",
    status_code=status.HTTP_200_OK,
)
async def delete_food(*, deps:CommonDeps, food_id: int):
    data = await get_food_id(deps=deps, food_id=food_id)

    data = await crud.delete(_id=food_id, db=deps['db'], db_obj=data)
    return
