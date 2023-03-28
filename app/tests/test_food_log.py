from sqlalchemy.orm import Session
from fastapi.testclient import TestClient
from fastapi.encoders import jsonable_encoder
from app.crud import crud
from app import models
from app import schemas
from datetime import date
from . import utils

async def test_food_log_create(client:TestClient, module_profile:models.Profile, serving, db:Session):
    data = {
        "date": date(2023,1,23).isoformat(), 
        "food_id": serving['food_id'],
        "serving_size_id": serving['id'],
        "serving_amount": 1,
        "profile_id": module_profile['id']
    }
    response= await client.post(f"/api/v1/food_log", json=data)
    assert response.status_code == 201
    content = response.json()
    assert "id" in content
    assert "serving_size" in content
    for key in data.keys():
        assert content[key] == data[key]

async def test_food_log_read_day(client:TestClient, db:Session, food_log:models.Food_Log):
    response= await client.get(f"/api/v1/food_log/date/{food_log['date']}")

    assert response.status_code == 200
    content = response.json()
    
    assert content['profile'] == food_log['profile']
    food_log.pop('profile')
    assert content['log'] == [food_log]

async def test_food_log_read_id(client:TestClient, db:Session, food_log:models.Food_Log):
    response= await client.get(f"/api/v1/food_log/{food_log['id']}")

    assert response.status_code == 200
    content = response.json()
    assert content == jsonable_encoder(food_log)

async def test_food_update(client:TestClient, db:Session, food_log:models.Food_Log):
    food_log['serving_amount'] += 2
    response = await client.put(f"/api/v1/food_log/{food_log['id']}", json=food_log)

    assert response.status_code == 200
    
    content = response.json()

    assert "serving_size" in content

    for key in food_log.keys():
        assert content[key] == food_log[key]

async def test_food_delete(client:TestClient, db:Session, food_log:models.Food_Log):
    response = await client.delete(f"/api/v1/food_log/{food_log['id']}")

    assert response.status_code == 200

    assert response.json() is None

    assert await crud.read(_id=food_log['id'], db=db, model=models.Food_Log) is None