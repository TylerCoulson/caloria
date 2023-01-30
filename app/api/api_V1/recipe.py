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
def post_recipe(*, recipe: schemas.RecipeCreate, db: Session = Depends(deps.get_db)):
    data = crud.read(_id=recipe.finished_food, db=db, model=models.Food)
    ingredient = crud.read(_id=recipe.ingredient, db=db, model=models.Food)
    data.ingredients.append(ingredient)
    db.add(data)
    db.commit()
    food_out = crud.read(_id=recipe.finished_food, db=db, model=models.Food)
    
    return food_out

# @router.get(
#     "/{food_id}",
#     response_model=schemas.Food,
#     status_code=status.HTTP_200_OK,
# )
# def get_food_id(*, food_id: int, db: Session = Depends(deps.get_db)):
#     data = crud.read(_id=food_id, db=db, model=models.Food)
#     if not data:
#         raise HTTPException(status_code=404, detail="Food not found")
#     return data

