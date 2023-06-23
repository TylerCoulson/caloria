from sqlalchemy.orm import Session
from fastapi.testclient import TestClient
from fastapi.encoders import jsonable_encoder
from app.crud import crud
from app import models
from app import schemas
import pytest


create_data = {"id": 1001, "food_id": 1, "description": 'nisi volutpat', "calories": 6121, "fats": 302, "carbs": 750, "protein": 372,}
update_data = {"id": 1, "food_id": 17, "description": 'amet', "calories": 9602, "fats": 332, "carbs": 571, "protein": 856}
update_food = {"id": 17, "category": 3, "type": 'nec sem', "subtype": 'magna'}
get_servings = {"id": 13, "food_id": 13, "description": 'lacus', "calories": 186, "fats": 369, "carbs": 764, "protein": 994}
get_servings_food = {"id": 13, "category": 6, "type": 'fermentum justo nec', "subtype": None}
get_data = {"id": 1, "food_id": 1, "description": 'nisi volutpat', "calories": 6121, "fats": 302, "carbs": 750, "protein": 372,}
food = {"id": 1, "category": 2, "type": 'posuere', "subtype": 'viverra dapibus'}
delete_id = 22



@pytest.mark.anyio
async def test_serving_size_create(client:TestClient, db:Session):
    response= await client.post(f"/api/v1/food/{create_data['food_id']}/serving", json=create_data)
    
    assert response.status_code == 201
    assert response.json() == {**create_data, "food":food}


@pytest.mark.anyio
async def test_serving_size_read_id(client:TestClient, db:Session):
    response= await client.get(f"/api/v1/food/{get_data['food_id']}/serving/{get_data['id']}")
    assert response.status_code == 200
    
    content = response.json() 
    assert content == {**get_data, "food":food}

@pytest.mark.anyio
async def test_serving_size_read_by_food(client:TestClient, db:Session):
    response= await client.get(f"/api/v1/food/{get_servings['food_id']}/servings")


    assert response.status_code == 200
    print(response.json())
    assert response.json() == {"servings": [{**get_servings, "food":get_servings_food}]}


@pytest.mark.anyio
async def test_serving_size_update(client:TestClient, db:Session):
    response= await client.put(f"/api/v1/food/{update_data['food_id']}/serving/{update_data['id']}", json=update_data)
    assert response.status_code == 200
    assert response.json() == {**update_data, "food":update_food}

@pytest.mark.anyio
async def test_serving_size_delete(client:TestClient, db:Session):
    response = await client.delete(f"/api/v1/food/{delete_id}/serving/{delete_id}")

    assert response.status_code == 200

    assert response.json() is None
    
    assert await crud.read(_id=delete_id, db=db, model=models.ServingSize) is None