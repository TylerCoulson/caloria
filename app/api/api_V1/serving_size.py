from fastapi import status, HTTPException
from sqlalchemy import select
from app import schemas
from app import models
from app import crud
from app.api.api_V1.deps import CommonDeps
from app.api.api_V1.food import router

router.tags = ['servings']

@router.post(
    "/{food_id}/serving",
    response_model=schemas.ServingSize,
    status_code=status.HTTP_201_CREATED,
)
async def post_serving_size(*, deps:CommonDeps, serving_size: schemas.ServingSizeCreate):
    serving_size_out = await crud.create(obj_in=serving_size, db=deps['db'], model=models.ServingSize)
    return serving_size_out

@router.get(
    "/{food_id}/serving/{serving_id}",
    response_model=schemas.ServingSize,
    status_code=status.HTTP_200_OK,
)
async def get_serving_size_id(*, deps:CommonDeps, food_id: int, serving_id: int):
    data = await crud.read(_id=serving_id, db=deps['db'], model=models.ServingSize)
    if not data:
        raise HTTPException(status_code=404, detail="Serving size not found")
    return data

@router.get(
    "/{food_id}/servings",
    response_model=schemas.AllServings,
    status_code=status.HTTP_200_OK,
)
async def get_serving_size_by_food(*, deps:CommonDeps, food_id: int):
    statement = select(models.ServingSize).where(models.ServingSize.food_id == food_id)

    data = await deps['db'].execute(statement)
    servings = data.unique().all()
    return {"servings":[value.__dict__ for value, in servings]}

@router.put(
    "/{food_id}/serving/{serving_id}",
    response_model=schemas.ServingSize,
    status_code=status.HTTP_200_OK,
)
async def update_serving_size(*, deps:CommonDeps, serving_id: int, serving_size_in: schemas.ServingSizeBase):

    data = await crud.update(_id=serving_id, model=models.ServingSize, update_data=serving_size_in, db=deps['db'])
    if not data:
        raise HTTPException(status_code=404, detail="Serving size not found")
    return data


@router.delete(
    "/{food_id}/serving/{serving_id}",
    status_code=status.HTTP_200_OK,
)
async def delete_serving_size(*, deps:CommonDeps, food_id:int, serving_id:int):
    data = await get_serving_size_id(deps=deps, food_id=food_id, serving_id=serving_id)
    data = await crud.delete(_id=serving_id, db=deps['db'], db_obj=data)
    
    return
