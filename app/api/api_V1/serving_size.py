from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session  # type: ignore

from app import deps
from app import schemas
from app import models

router = APIRouter()

from app import crud


@router.post(
    "",
    response_model=schemas.ServingSize,
    status_code=status.HTTP_201_CREATED,
)
def post_serving_size(*, serving_size: schemas.ServingSizeCreate, db: Session = Depends(deps.get_db)):
    serving_size_out = crud.create(obj_in=serving_size, db=db, model=models.ServingSize)
    return serving_size_out

@router.get(
    "/{serving_size_id}",
    response_model=schemas.ServingSize,
    status_code=status.HTTP_200_OK,
)
def get_serving_size_id(*, serving_size_id: int, db: Session = Depends(deps.get_db)):
    data = crud.read(_id=serving_size_id, db=db, model=models.ServingSize)
    if not data:
        raise HTTPException(status_code=404, detail="serving size not found")
    return data

@router.get(
    "/food_id/{food_id}",
    response_model=schemas.AllServings,
    status_code=status.HTTP_200_OK,
)
def get_serving_size_by_food(*, food_id: int, db: Session = Depends(deps.get_db)) -> list[schemas.FoodLog]:
    data = db.query(models.ServingSize).filter(models.ServingSize.food_id == food_id).all()
    
    # if not data:
    #     raise HTTPException(status_code=404, detail="Serving Size not found")

    return {"servings": data}


# @router.put(
#     "/{serving_size_id}",
#     response_model=schemas.ServingSizeBase,
#     status_code=status.HTTP_200_OK,
# )
# def update_serving_size(
#     *, serving_size_id: int, serving_size_in: schemas.ServingSizeBase, db: Session = Depends(deps.get_db)
# ):
#     data = get_serving_size(serving_size_id=serving_size_id, db=db)

#     data = crud.update(db_obj=data, data_in=serving_size_in, db=db)
#     return data


# @router.delete(
#     "/{serving_size_id}",
#     status_code=status.HTTP_200_OK,
# )
# def delete_serving_size(*, serving_size_id: int, db: Session = Depends(deps.get_db)):
#     data = get_serving_size(serving_size_id=serving_size_id, db=db)

#     data = crud.delete(_id=serving_size_id, db=db, db_obj=data)
#     return data
