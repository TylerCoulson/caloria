from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session  # type: ignore
from app import deps
from app import schemas
from app import models

router = APIRouter()

from app import crud


@router.post(
    "",
    response_model=schemas.Food,
    status_code=status.HTTP_201_CREATED,
)
def post_food(*, food: schemas.FoodCreate, db: Session = Depends(deps.get_db)):
    food_out = crud.create(obj_in=food, db=db, model=models.Food)
    return food_out

@router.get(
    "/{food_id}",
    response_model=schemas.Food,
    status_code=status.HTTP_200_OK,
)
def get_food_id(*, food_id: int, db: Session = Depends(deps.get_db)):
    data = crud.read(_id=food_id, db=db, model=models.Food)
    if not data:
        raise HTTPException(status_code=404, detail="Food not found")
    return data

@router.get(
    "/search",
    response_model=schemas.Food,
    status_code=status.HTTP_200_OK,
)
def get_food_search(*, search_for:str, search_word:str, n:int=25, db: Session = Depends(deps.get_db)):
    data = db.query(models.Food).filter(getattr(models.Food, search_for).contains(search_word)).limit(n).all()
    if not data:
        raise HTTPException(status_code=404, detail="Food not found")
    return data

@router.get(
    "/all",
    response_model=schemas.Food,
    status_code=status.HTTP_200_OK,
)
def get_all_foods(*, n:int=25, db: Session = Depends(deps.get_db)):
    data = db.query(models.Food).filter().limit(n).all()
    return data

@router.put(
    "/{food_id}",
    response_model=schemas.Food,
    status_code=status.HTTP_200_OK,
)
def update_food(
    *, food_id: int, food_in: schemas.FoodBase, db: Session = Depends(deps.get_db)
):
    data = get_food_id(food_id=food_id, db=db)

    data = crud.update(db_obj=data, data_in=food_in, db=db)

    return data


@router.delete(
    "/{food_id}",
    status_code=status.HTTP_200_OK,
)
def delete_food(*, food_id: int, db: Session = Depends(deps.get_db)):
    data = get_food_id(food_id=food_id, db=db)

    data = crud.delete(_id=food_id, db=db, db_obj=data)
    return
