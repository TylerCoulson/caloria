from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session  # type: ignore
from sqlalchemy import select
from app import deps
from app import schemas
from app import models
from app import crud
from fastapi.encoders import jsonable_encoder
from app.api.api_V1.food import router
router.tags = ['servings']

@router.post(
    "/{food_id}/serving",
    response_model=schemas.ServingSize,
    status_code=status.HTTP_201_CREATED,
)
async def post_serving_size(*, serving_size: schemas.ServingSizeCreate, db: Session = Depends(deps.get_db)):
    serving_size_out = await crud.create(obj_in=serving_size, db=db, model=models.ServingSize)
    return serving_size_out

@router.get(
    "/{food_id}/serving/{serving_id}",
    response_model=schemas.ServingSize,
    status_code=status.HTTP_200_OK,
)
async def get_serving_size_id(*, serving_id: int, db: Session = Depends(deps.get_db)):

    data = await crud.read(_id=serving_id, db=db, model=models.ServingSize)

    if not data:
        raise HTTPException(status_code=404, detail="serving size not found")
    return data

@router.get(
    "/{food_id}/servings",
    response_model=schemas.AllServings,
    status_code=status.HTTP_200_OK,
)
async def get_serving_size_by_food(*, food_id: int, db: Session = Depends(deps.get_db)):
    statement = select(models.ServingSize).where(models.ServingSize.food_id == food_id)

    data = await db.execute(statement)
    test = data.unique().all()

    return {"servings":[value for value, in test]}

@router.put(
    "/{food_id}/serving/{serving_id}",
    response_model=schemas.ServingSize,
    status_code=status.HTTP_200_OK,
)
async def update_serving_size(
    *, serving_id: int, serving_size_in: schemas.ServingSizeBase, db: Session = Depends(deps.get_db)
):
    data = await get_serving_size_id(serving_id=serving_id, db=db)

    data = await crud.update(db_obj=data, data_in=serving_size_in, db=db)
    return data


@router.delete(
    "/{food_id}/serving/{serving_id}",
    status_code=status.HTTP_200_OK,
)
async def delete_serving_size(*, serving_id: int, db: Session = Depends(deps.get_db)):
    data = await get_serving_size_id(serving_id=serving_id, db=db)
    data = await crud.delete(_id=serving_id, db=db, db_obj=data)
    return
