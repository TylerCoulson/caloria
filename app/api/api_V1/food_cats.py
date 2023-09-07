from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session  # type: ignore
from typing import List
from app import deps
from app import schemas
from app import models
from app.auth.router import Annotated_Superuser
router = APIRouter(tags=["food-categories"])

from app import crud


@router.post(
    "",
    response_model=schemas.FoodCategory,
    status_code=status.HTTP_201_CREATED,
)
async def create_category(*, super_user: Annotated_Superuser, cat:schemas.FoodCategoryCreate, db: Session = Depends(deps.get_db)):
    
    food_out = await crud.create(obj_in=cat, db=db, model=models.FoodCategories)
    return food_out

@router.get(
    "",
    response_model=List[schemas.FoodCategory],
    status_code=status.HTTP_200_OK,
)
async def get_all_categories(*, n:int=25, page:int=1, db: Session = Depends(deps.get_db)):
    return await crud.read_all(n=n, page=page, db=db, model=models.FoodCategories)

@router.put(
    "/{id}",
    status_code=status.HTTP_200_OK,
)
async def update_categories(*, super_user: Annotated_Superuser, id: int, cat_in: schemas.FoodCategoryCreate, db: Session = Depends(deps.get_db)
):
    data = await crud.update(_id=id, model=models.FoodCategories, update_data=cat_in, db=db)
    
    if data is None:
        raise HTTPException(status_code=404, detail="No category with this id")
    return data

@router.delete(
    "/all",
    status_code=status.HTTP_200_OK,
)
async def delete_categories(*, super_user: Annotated_Superuser, n:int=25, page:int=1, db: Session = Depends(deps.get_db)):
    data = await crud.read_all(n=n, page=page, db=db, model=models.FoodCategories)
    for i in data:
        await crud.delete(_id=i.id, db=db, db_obj=i)
    return 

