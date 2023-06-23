from sqlalchemy.orm import Session
from fastapi.testclient import TestClient
from httpx import AsyncClient
from app.crud import crud
from app import models
from app import schemas
from datetime import date

get_data = {"id": 1, "category": 2, "type": 'posuere', "subtype": 'viverra dapibus'}
create_data = {"id": 1001, "category": 2, "type": 'odio porttitor', "subtype": 'nec'}
update_data = {"id": 1, "category": 2, "type": 'odio porttitor', "subtype": 'nec'}
delete_id = 10
all_check = {"id":6, "category": 6, "type": 'primis', "subtype": 'sit amet lobortis'}
search_result = {"id":42, "category": 6, "type": 'justo nec condimentum', "subtype": None}
async def test_food_create(client:AsyncClient, db:Session):

    response = await client.post(f"/api/v1/food", json=create_data)

    assert response.status_code == 201
    content = response.json()
    assert "id" in content

    assert content == create_data

async def test_food_read(client:AsyncClient, db:Session):

    response= await client.get(f"/api/v1/food/{get_data['id']}")
    assert response.status_code == 200
    assert response.json() == get_data


async def test_food_update(client:AsyncClient, db:Session):

    response = await client.put(f"/api/v1/food/{update_data['id']}", json=update_data)

    assert response.status_code == 200

    assert response.json() == update_data

async def test_food_delete(client:AsyncClient, db:Session):
    response = await client.delete(f"/api/v1/food/{delete_id}")

    assert response.status_code == 200

    assert response.json() is None

    assert await crud.read(_id=delete_id, db=db, model=models.Food) is None

async def test_get_all_foods(client):
    response = await client.get("/api/v1/food/all")
    content = response.json() 
    assert response.status_code == 200
    assert len(content) == 25
    assert content[5] == all_check


async def test_get_search_foods(client):
    response = await client.get("/api/v1/food/search?search_word=condimentum&n=25&page=1")
    content = response.json() 
    assert response.status_code == 200
    assert len(content) == 14
    assert content[0] == search_result