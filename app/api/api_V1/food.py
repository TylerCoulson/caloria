from fastapi import APIRouter, status, HTTPException
from typing import List
from sqlalchemy import select, func, or_, nulls_last
from app import schemas
from app import models
from app.api.api_V1.deps import CommonDeps, LoggedInDeps
from app import crud
from app.api.api_V1 import utils

router = APIRouter(tags=["food"])

#  ************
#  *  CREATE  *
#  ************
@router.post(
    "",
    response_model=schemas.Food,
    status_code=status.HTTP_201_CREATED,
)
async def post_food(*, deps:LoggedInDeps, food: schemas.FoodCreate):
    food.user_id = deps['user'].id

    food_out = await crud.create(obj_in=food, db=deps['db'], model=models.Food, profile=deps['profile'])
    return food_out

#  ************
#  *  READ    *
#  ************
@router.get(
    "/all",
    response_model=List[schemas.Food],
    status_code=status.HTTP_200_OK,
)
async def get_all_foods(*, deps:CommonDeps, n:int=25, page:int=1):
    statement = utils.get_all_statement(deps=deps, n=n, page=page)

    data = await deps['db'].execute(statement)
    
    all_data = data.unique().all()

    return [value for value, in all_data]



@router.get(
    "/search",
    response_model=List[schemas.Food],
    status_code=status.HTTP_200_OK,
)
async def get_food_search(*, deps:CommonDeps, search_word:str, n:int=25, page:int=1):
    statement = utils.get_all_statement(deps=deps, n=n, page=page
        ).where(
        func.lower(models.Food.type).contains(search_word) | func.lower(models.Food.subtype).contains(search_word) 
    )

    data = await deps['db'].execute(statement)
    
    all_data = data.unique().all()

    return [value for value, in all_data]



@router.get(
        "/types",
        response_model=List[schemas.FoodNoSubtype],
        status_code=status.HTTP_200_OK
)
async def get_food_types(*, deps:CommonDeps, n:int=25, page:int=1):
    statement = utils.get_all_statement(deps=deps, n=n, page=page
        ).with_only_columns(models.Food.type, models.Food.user_id
        ).distinct(
        ).order_by(nulls_last(models.Food.user_id.desc()), models.Food.type
        )



    data = await deps['db'].execute(statement)
    
    result = data.unique().all()
    return [schemas.FoodNoSubtype(type=r[0]) for r in result]

@router.get(
        "/{food_type:str}/subtypes",
        response_model=List[schemas.Food],
        status_code=status.HTTP_200_OK
)
async def get_food_subtypes(*, deps:CommonDeps, n:int=25, page:int=1, food_type:str):
    statement = utils.get_all_statement(deps=deps, n=n, page=page
        ).where(func.lower(models.Food.type) == food_type.lower()
        )


    data = await deps['db'].execute(statement)
    
    result = data.unique().all()

    return [r for r, in result]


@router.get(
    "/{food_id}",
    response_model=schemas.Food,
    status_code=status.HTTP_200_OK,
)
async def get_food_by_id(*, deps:CommonDeps, food_id: int):
    return await utils.get_food_by_id(deps=deps, food_id=food_id)


#  ************
#  *  UPDATE  *
#  ************
@router.put(
    "/{food_id}",
    response_model=schemas.Food,
    status_code=status.HTTP_200_OK,
)
async def update_food(
    *, deps:LoggedInDeps, food_id: int, food_in: schemas.FoodBase
):
    food = await get_food_by_id(deps=deps, food_id=food_id)

    if food.user_id is None:
        raise HTTPException(status_code=404, detail="Cannot modify this Food")

    data = await crud.update(_id=food_id, model=models.Food, update_data=food_in, db=deps['db'], profile=deps['profile'])

    return data



#  ************
#  *  Delete  *
#  ************
@router.delete(
    "/{food_id}",
    status_code=status.HTTP_200_OK,
)
async def delete_food(*, deps:LoggedInDeps, food_id: int):
    user_id = utils.get_user_id(deps=deps)
    data = await get_food_by_id(deps=deps, food_id=food_id)

    if user_id != data.user_id:
        raise HTTPException(status_code=404, detail="No food with this id")

    data = await crud.delete(_id=food_id, db=deps['db'], db_obj=data)
    return
