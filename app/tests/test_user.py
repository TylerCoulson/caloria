from sqlalchemy.orm import Session
from fastapi.testclient import TestClient
from fastapi.encoders import jsonable_encoder
from app import models
from app import schemas
from app import crud
from . import utils


def test_user_create(client:TestClient, db:Session):
    data = utils.create_random_user_dict()

    response= client.post(f"/api/v1/user", json=data)
    
    assert response.status_code == 201
    content = response.json()
    assert "id" in content

    for key in data.keys():
        assert content[key] == data[key]


def test_user_read(client:TestClient, db:Session, user:models.User):

    response= client.get(f"/api/v1/user/{user.id}")
    content = response.json()
    assert response.status_code == 200
    
    assert content == jsonable_encoder(user)

def test_users_food_logs(client:TestClient, db:Session, food_log:models.Food_Log):

    response= client.get(f"/api/v1/user/{food_log.user_id}")
    assert response.status_code == 200
 
    content = response.json()
    assert content['log'] == [jsonable_encoder(food_log)]

def test_duplicate_user(client:TestClient, db:Session, user:models.User):

    data = jsonable_encoder(schemas.UserCreate(**jsonable_encoder(user)))
    response= client.post(f"/api/v1/user", json=data)
    assert response.status_code == 403

    content = response.json()

    assert content == {'detail': 'Email already has an account'}

def test_update_user(client:TestClient, db:Session, user:models.User):
    user.end_weight += 52
    data = jsonable_encoder(schemas.UserCreate(**jsonable_encoder(user)))

    response= client.put(f"/api/v1/user/{user.id}", json=data)

    assert response.status_code == 200

    content = response.json()

    assert content == jsonable_encoder(user)


def test_user_delete(client:TestClient, db:Session, user:models.User):
    response = client.delete(f"/api/v1/user/{user.id}")

    assert response.status_code == 200

    assert response.json() is None

    assert crud.read(_id=user.id, db=db, model=models.Food_Log) is None