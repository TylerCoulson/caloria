from sqlalchemy.orm import Session
from fastapi.testclient import TestClient
from fastapi.encoders import jsonable_encoder
from app.crud import crud
from app import models
from app import schemas
from datetime import date
from . import utils

create_data = {"id":1001, "date":'2022-12-09', "food_id":123, "serving_size_id":123, "serving_amount":3, "profile_id":1}
profile = {"id":1, "start_date": '2022-12-06', "start_weight": 322.4, "goal_weight": 150.0, "sex": 'Male', "birthdate": '1992-12-05', "height": 70, "lbs_per_week": 2.0, "activity_level": 2.0, "user_id": 1}
get_log = [{ "id":12, "date":'2022-10-09', "food_id":123, "serving_size_id":123, "serving_amount":3.0, "profile_id":1,}, { "id":97, "date":'2022-10-09', "food_id":813, "serving_size_id":813, "serving_amount":9.0, "profile_id":1,}, { "id":429, "date":'2022-10-09', "food_id":426, "serving_size_id":426, "serving_amount":85.0, "profile_id":1,}, { "id":713, "date":'2022-10-09', "food_id":571, "serving_size_id":571, "serving_amount":25.0, "profile_id":1, }]
get_log_date = "2022-10-09"
update_data = {"id":17, "date":'2023-04-27', "food_id":123, "serving_size_id":123, "serving_amount":4.0, "profile_id":1}
delete_id = 18
keys = ["id", "date", "food_id", "serving_size_id", "serving_amount", "profile_id"]

async def test_food_log_create(client:TestClient):
    data = {**create_data, "profile_id":1}
    response = await client.post(f"/api/v1/food_log", json=data)
    assert response.status_code == 201
    content = response.json()
    assert content['profile'] == profile
    assert "serving_size" in content
    for key in keys:
        assert content[key] == create_data[key]

async def test_food_log_read_day(client:TestClient, db:Session):
    response= await client.get(f"/api/v1/food_log/date/{get_log_date}")

    assert response.status_code == 200
    content = response.json()

    assert content['profile'] == profile
    for log in content['log']:
        assert "serving_size" in log
        log.pop('serving_size')
        assert log in get_log

async def test_food_log_read_id(client:TestClient, db:Session):
    response= await client.get(f"/api/v1/food_log/{get_log[0]['id']}")

    assert response.status_code == 200
    content = response.json()

    assert content['profile'] == profile
    assert "serving_size" in content
    for key in keys:
        assert content[key] == get_log[0][key]

async def test_food_log_update(client:TestClient, db:Session):
    response = await client.put(f"/api/v1/food_log/{update_data['id']}", json=update_data)

    assert response.status_code == 200
    
    content = response.json()

    assert content['profile'] == profile
    assert "serving_size" in content
    for key in keys:
        assert content[key] == update_data[key]

async def test_food_delete(client:TestClient, db:Session):
    response = await client.delete(f"/api/v1/food_log/{delete_id}")

    assert response.status_code == 200

    assert response.json() is None

    assert await crud.read(_id=delete_id, db=db, model=models.Food_Log) is None