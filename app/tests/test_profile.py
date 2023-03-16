from sqlalchemy.orm import Session
from fastapi.testclient import TestClient
from fastapi.encoders import jsonable_encoder
from app import models
from app import schemas
from app import crud
from . import utils
from datetime import date

async def test_profile_create(client:TestClient, db:Session, module_user):
    start_date = date(2022,12,6)
    password_hash = "password"
    email = f"user@example.com"
    start_weight = 322.4
    goal_weight = 150
    sex = 'male'
    birthdate = date(1992,12,5)
    height = 70
    lbs_per_week = 1.2
    activity_level = 1.2

    data = schemas.ProfileBase(
        start_date=start_date,
        password_hash=password_hash,
        email=email,
        start_weight=start_weight,
        goal_weight=goal_weight,
        sex=sex,
        birthdate=birthdate,
        height=height,
        lbs_per_week=lbs_per_week,
        activity_level=activity_level,
    )

    data = jsonable_encoder(data)
    response= await client.post(f"/api/v1/profile", json=data)
    
    assert response.status_code == 201
    content = response.json()
    assert "id" in content

    for key in data.keys():
        assert content[key] == data[key]


async def test_profile_read(client:TestClient, db:Session, module_profile):
    response= await client.get(f"/api/v1/profile/me")
    content = response.json()
    assert response.status_code == 200
    
    assert content == jsonable_encoder(module_profile)

async def test_profiles_food_logs(client:TestClient, db:Session, food_log:models.Food_Log):

    response= await client.get(f"/api/v1/profile/me")
    assert response.status_code == 200

    content = response.json()
 
    for k, v in food_log['profile'].items():
        assert content[k] == v
    food_log.pop('profile')
    assert content['log'] == [food_log]

async def test_update_profile(client:TestClient, db:Session, module_profile:models.Profile):
    module_profile['goal_weight'] += 52
    data = jsonable_encoder(schemas.ProfileCreate(**jsonable_encoder(module_profile)))

    response= await client.put(f"/api/v1/profile/me", json=data)

    assert response.status_code == 200

    content = response.json()
    fix_data = jsonable_encoder(module_profile)
    fix_data.pop('log')
    assert content == fix_data


async def test_profile_delete(client:TestClient, db:Session, module_profile:models.Profile):
    response = await client.delete(f"/api/v1/profile/me")
    assert response.status_code == 200

    assert response.json() is None

    assert await crud.read(_id=module_profile['id'], db=db, model=models.Food_Log) is None
