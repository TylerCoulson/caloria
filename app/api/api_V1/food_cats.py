from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session  # type: ignore
from typing import List
from app import deps
from app import schemas
from app import models
from app.auth.router import Annotated_Superuser
from app.api.api_V1.deps import LoggedInDeps, CommonDeps

router = APIRouter(tags=["food-categories"])

from app import crud

# #  ************
# #  *  CREATE  *
# #  ************
# @router.post(
#     "",
#     response_model=schemas.FoodCategory,
#     status_code=status.HTTP_201_CREATED,
# )
# async def create_category(*, deps:LoggedInDeps, super_user: Annotated_Superuser, cat:schemas.FoodCategoryCreate):
    
#     food_out = await crud.create(obj_in=cat, db=deps['db'], model=models.FoodCategories, profile=deps['profile'])
#     return food_out


#  ************
#  *  READ    *
#  ************
@router.get(
    "",
    response_model=List[schemas.FoodCategory],
    status_code=status.HTTP_200_OK,
)
async def get_all_categories(*, deps:CommonDeps, n:int=25, page:int=1):
    return await crud.read_all(n=n, page=page, db=deps['db'], model=models.FoodCategories)


# #  ************
# #  *  UPDATE  *
# #  ************
# @router.put(
#     "/{id}",
#     status_code=status.HTTP_200_OK,
# )
# async def update_categories(*, deps:LoggedInDeps, super_user: Annotated_Superuser, id: int, cat_in: schemas.FoodCategoryCreate):
#     data = await crud.update(_id=id, model=models.FoodCategories, update_data=cat_in, db=deps['db'], profile=deps['profile'])
    
#     if data is None:
#         raise HTTPException(status_code=404, detail="No category with this id")
#     return data


# #  ************
# #  *  Delete  *
# #  ************
# @router.delete(
#     "/all",
#     status_code=status.HTTP_200_OK,
# )
# async def delete_categories(*, deps:LoggedInDeps, super_user: Annotated_Superuser, n:int=25, page:int=1):
#     data = await crud.read_all(n=n, page=page, db=deps['db'], model=models.FoodCategories)
#     for i in data:
#         await crud.delete(_id=i.id, db=deps['db'], db_obj=i)
#     return 

