from sqlalchemy.orm import Session
from fastapi.testclient import TestClient
from fastapi.encoders import jsonable_encoder
from app import models
from app import schemas
from app import crud
from . import utils


def test_profile_create(client:TestClient, db:Session):
    data = utils.create_random_profile_dict()

    response= client.post(f"/api/v1/profile", json=data)
    
    assert response.status_code == 201
    content = response.json()
    assert "id" in content

    for key in data.keys():
        assert content[key] == data[key]


def test_profile_read(client:TestClient, db:Session, profile:models.Profile):

    response= client.get(f"/api/v1/profile/{profile.id}")
    content = response.json()
    assert response.status_code == 200
    
    assert content == jsonable_encoder(profile)

def test_profiles_food_logs(client:TestClient, db:Session, food_log:models.Food_Log):

    response= client.get(f"/api/v1/profile/{food_log.profile_id}")
    assert response.status_code == 200
 
    content = response.json()
    assert content['log'] == [jsonable_encoder(food_log)]

def test_duplicate_profile(client:TestClient, db:Session, profile:models.Profile):

    data = jsonable_encoder(schemas.ProfileCreate(**jsonable_encoder(profile)))
    response= client.post(f"/api/v1/profile", json=data)
    assert response.status_code == 403

    content = response.json()

    assert content == {'detail': 'Email already has an account'}

def test_update_profile(client:TestClient, db:Session, profile:models.Profile):
    profile.goal_weight += 52
    data = jsonable_encoder(schemas.ProfileCreate(**jsonable_encoder(profile)))

    response= client.put(f"/api/v1/profile/{profile.id}", json=data)

    assert response.status_code == 200

    content = response.json()

    assert content == jsonable_encoder(profile)


def test_profile_delete(client:TestClient, db:Session, profile:models.Profile):
    response = client.delete(f"/api/v1/profile/{profile.id}")

    assert response.status_code == 200

    assert response.json() is None

    assert crud.read(_id=profile.id, db=db, model=models.Food_Log) is None