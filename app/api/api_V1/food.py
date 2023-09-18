from fastapi import APIRouter, status, HTTPException
from typing import List
from sqlalchemy import select, func, or_
from app import schemas
from app import models
from app.api.api_V1.deps import CommonDeps, LoggedInDeps
from app import crud


router = APIRouter(tags=["food"])

def get_user_id(deps:CommonDeps):
    return None if deps['user'] is None else deps['user'].id

@router.post(
    "",
    response_model=schemas.Food,
    status_code=status.HTTP_201_CREATED,
)
async def post_food(*, deps:LoggedInDeps, food: schemas.FoodCreate):
    food.user_id = deps['user'].id

    food_out = await crud.create(obj_in=food, db=deps['db'], model=models.Food)
    return food_out

@router.get(
    "/search",
    response_model=List[schemas.Food],
    status_code=status.HTTP_200_OK,
)
async def get_food_search(*, deps:CommonDeps, search_word:str, n:int=25, page:int=1):
    if n < 0:
        n = 25
    user_id = get_user_id(deps=deps)
    
    offset = max((page-1) * n, 0)

    statement = select(models.Food).where(
        func.lower(models.Food.type).contains(search_word) | func.lower(models.Food.subtype).contains(search_word) 
    ).where(or_(models.Food.user_id == user_id, models.Food.user_id == None) 
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
    if n < 0:
        n = 25
    offset = max((page-1) * n, 0)
    user_id = get_user_id(deps=deps)
    statement = select(models.Food).where(or_(models.Food.user_id == user_id, models.Food.user_id == None) 
    ).limit(n
    ).offset(offset)

    data = await deps['db'].execute(statement)
    
    all_data = data.unique().all()

    return [value for value, in all_data]

@router.get(
    "/{food_id}",
    response_model=schemas.Food,
    status_code=status.HTTP_200_OK,
)
async def get_food_id(*, deps:CommonDeps, food_id: int):
    user_id = get_user_id(deps=deps)
    data = await crud.read(_id=food_id, db=deps['db'], model=models.Food)
    
    if not data or (user_id != data.user_id and data.user_id is not None):
        raise HTTPException(status_code=404, detail="Food not found")
    return data

@router.put(
    "/{food_id}",
    response_model=schemas.Food,
    status_code=status.HTTP_200_OK,
)
async def update_food(
    *, deps:LoggedInDeps, food_id: int, food_in: schemas.FoodBase
):
    user_id = get_user_id(deps=deps)
    data = await crud.update(_id=food_id, model=models.Food, update_data=food_in, db=deps['db'])
    
    if data is None or user_id != data.user_id:
        raise HTTPException(status_code=404, detail="No food with this id")
    return data


@router.delete(
    "/{food_id}",
    status_code=status.HTTP_200_OK,
)
async def delete_food(*, deps:LoggedInDeps, food_id: int):
    user_id = get_user_id(deps=deps)
    data = await get_food_id(deps=deps, food_id=food_id)

    if user_id != data.user_id:
        raise HTTPException(status_code=404, detail="No food with this id")

    data = await crud.delete(_id=food_id, db=deps['db'], db_obj=data)
    return
