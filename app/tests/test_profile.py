from sqlalchemy.orm import Session
from fastapi.testclient import TestClient
from fastapi.encoders import jsonable_encoder
from app import models
from app import schemas
from app import crud
from . import utils
from datetime import date

create_profile = {"id":1001, "start_date": '2023-04-09', "start_weight": 803.3, "goal_weight": 241.0, "sex": 'Male', "birthdate": '1994-10-26', "height": 10, "lbs_per_week": 1.38, "activity_level": 1.8, "user_id": 1001}
read_profile = {"id":1, "start_date": '2023-04-09', "start_weight": 803.3, "goal_weight": 241.0, "sex": 'Male', "birthdate": '1994-10-26', "height": 10, "lbs_per_week": 1.38, "activity_level": 1.8, "user_id": 1}


async def test_profile_create(client:TestClient, db:Session, module_user):
    response= await client.post(f"/api/v1/profile", json=create_profile)
    
    assert response.status_code == 201
    assert response.json() == create_profile


async def test_profile_read(client:TestClient, db:Session):
    response= await client.get(f"/api/v1/profile/me")
    assert response.status_code == 200
    assert response.json() == read_profile


async def test_profile_food_logs(client:TestClient, db:Session):

    response= await client.get(f"/api/v1/profile/me/logs")
    assert response.status_code == 200

    content = response.json() 

    assert "logs" in content

async def test_profile_update(client:TestClient, db:Session, module_profile:models.Profile):
    module_profile['goal_weight'] += 52
    data = jsonable_encoder(module_profile)

    response= await client.put(f"/api/v1/profile/me", json=data)

    assert response.status_code == 200

    content = response.json()
    fix_data = jsonable_encoder(module_profile)
    assert content == fix_data


async def test_profile_delete(client:TestClient, db:Session, module_profile:models.Profile):
    response = await client.delete(f"/api/v1/profile/me")
    assert response.status_code == 200

    assert response.json() is None

    assert await crud.read(_id=module_profile['id'], db=db, model=models.Food_Log) is None
