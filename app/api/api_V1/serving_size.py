from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session  # type: ignore

from app import deps
from app import schemas
from app import models
from app import crud

from app.api.api_V1.food import router
router.tags = ['servings']

@router.post(
    "/{food_id}/serving",
    response_model=schemas.ServingSize,
    status_code=status.HTTP_201_CREATED,
)
def post_serving_size(*, serving_size: schemas.ServingSizeCreate, db: Session = Depends(deps.get_db)):
    serving_size_out = crud.create(obj_in=serving_size, db=db, model=models.ServingSize)
    return serving_size_out

@router.get(
    "/{food_id}/serving/{serving_id}",
    response_model=schemas.ServingSize,
    status_code=status.HTTP_200_OK,
)
def get_serving_size_id(*, serving_id: int, db: Session = Depends(deps.get_db)):
    print("TESTING")
    data = crud.read(_id=serving_id, db=db, model=models.ServingSize)
    if not data:
        raise HTTPException(status_code=404, detail="serving size not found")
    return data

@router.get(
    "/{food_id}/servings",
    response_model=schemas.AllServings,
    status_code=status.HTTP_200_OK,
)
def get_serving_size_by_food(*, food_id: int, db: Session = Depends(deps.get_db)) -> list[schemas.FoodLog]:
    data = db.query(models.ServingSize).filter(models.ServingSize.food_id == food_id).all()

    return {"servings": data}


@router.put(
    "/{food_id}/serving/{serving_id}",
    response_model=schemas.ServingSize,
    status_code=status.HTTP_200_OK,
)
def update_serving_size(
    *, serving_id: int, serving_size_in: schemas.ServingSizeBase, db: Session = Depends(deps.get_db)
):
    data = get_serving_size_id(serving_id=serving_id, db=db)

    data = crud.update(db_obj=data, data_in=serving_size_in, db=db)
    return data


@router.delete(
    "/{food_id}/serving/{serving_id}",
    status_code=status.HTTP_200_OK,
)
def delete_serving_size(*, serving_id: int, db: Session = Depends(deps.get_db)):
    data = get_serving_size_id(serving_id=serving_id, db=db)

    data = crud.delete(_id=serving_id, db=db, db_obj=data)
    return
