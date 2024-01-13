from fastapi import status, HTTPException
from sqlalchemy import select
from app import schemas
from app import models
from app import crud
from app.api.api_V1.deps import CommonDeps
from app.api.api_V1.food import router
from app.api.api_V1 import utils

router.tags = ['servings']


#  ************
#  *  CREATE  *
#  ************
@router.post(
    "/{food_id}/serving",
    response_model=schemas.ServingSize,
    status_code=status.HTTP_201_CREATED,
)
async def post_serving_size(*, deps:CommonDeps, food_id:int, serving_size: schemas.ServingSizeCreate):

    food = await crud.read(_id=food_id, db=deps['db'], model=models.Food, profile=deps['profile'])
    if not food:
        raise HTTPException(status_code=404, detail="Food Not Found")

    serving_size_out = await crud.create(obj_in=serving_size, db=deps['db'], model=models.ServingSize)
    return serving_size_out


#  ************
#  *   READ   *
#  ************
@router.get(
    "/{food_id}/serving/{serving_id}",
    response_model=schemas.ServingSize,
    status_code=status.HTTP_200_OK,
)
async def get_serving_size_by_id(*, deps:CommonDeps, food_id: int=None, serving_id: int):
    food = await crud.read(_id=food_id, db=deps['db'], model=models.Food, profile=deps['profile'])
    if not food:
        raise HTTPException(status_code=404, detail="Food Not Found")
    
    data = await crud.read(_id=serving_id, db=deps['db'], model=models.ServingSize, profile=deps['profile'])

    if not data or data.food.id != food.id:
        raise HTTPException(status_code=404, detail="Serving size not found")

    # await utils.check_food_authorized(deps=deps, food=data.food)

    return data

@router.get(
    "/{food_id}/servings",
    response_model=schemas.AllServings,
    status_code=status.HTTP_200_OK,
)
async def get_serving_size_by_food(*, deps:CommonDeps, food_id: int):
    food = await crud.read(_id=food_id, db=deps['db'], model=models.Food, profile=deps['profile'])
    if not food:
        raise HTTPException(status_code=404, detail="Food Not Found")

    servings=food.servings

    return {"servings": servings}


#  ************
#  *  Update  *
#  ************
@router.put(
    "/{food_id}/serving/{serving_id}",
    response_model=schemas.ServingSize,
    status_code=status.HTTP_200_OK,
)
async def update_serving_size(*, deps:CommonDeps, food_id:int, serving_id: int, serving_size_in: schemas.ServingSizeBase):
    data = await crud.update(_id=serving_id, model=models.ServingSize, update_data=serving_size_in, db=deps['db'], profile=deps['profile'])
    if not data:
        raise HTTPException(status_code=404, detail="Serving size not found")
    return data



#  ************
#  *  Delete  *
#  ************
@router.delete(
    "/{food_id}/serving/{serving_id}",
    status_code=status.HTTP_200_OK,
)
async def delete_serving_size(*, deps:CommonDeps, food_id:int, serving_id:int):
    food = await crud.read(_id=food_id, db=deps['db'], model=models.Food, profile=deps['profile'])
    if not food:
        raise HTTPException(status_code=404, detail="Food Not Found")

    data = await crud.delete(_id=serving_id, db=deps['db'], model=models.ServingSize, profile=deps['profile'])
    if not data:
        raise HTTPException(status_code=404, detail="Food Not Found")
    return
