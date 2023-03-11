from sqlalchemy.orm import Session
from fastapi.testclient import TestClient
from httpx import AsyncClient
from app.crud import crud
from app import models
from app import schemas
from datetime import date


async def test_food_create(client:AsyncClient, db:Session):
    data = {
        "brand": "generic",
        "name": "test123"
    }

    response= await client.post(f"/api/v1/food", json=data)

    assert response.status_code == 201
    content = response.json()
    assert "id" in content

    for key in data.keys():
        assert content[key] == data[key]

async def test_food_read(client:AsyncClient, db:Session, food:schemas.Food):

    response= await client.get(f"/api/v1/food/{food['id']}")
    assert response.status_code == 200
    assert response.json() == {
        "id": food['id'],
        "brand": food['brand'],
        "name": food['name'],
        "ingredients": []
    }


async def test_food_update(client:AsyncClient, db:Session, food:schemas.Food):
    data = {
        "brand": "read_test",
        "name": "test123"
    }

    response = await client.put(f"/api/v1/food/{food['id']}", json=data)

    assert response.status_code == 200

    assert response.json() == {
        "id": food['id'],
        "brand": data['brand'],
        "name": data['name'],
        "ingredients": []
    }

async def test_food_delete(client:AsyncClient, db:Session, food:schemas.Food):
    response = await client.delete(f"/api/v1/food/{food['id']}")

    assert response.status_code == 200

    assert response.json() is None

    assert await crud.read(_id=food['id'], db=db, model=models.Food) is None