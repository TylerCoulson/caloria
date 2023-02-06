from sqlalchemy.orm import Session
from fastapi.testclient import TestClient

from . import utils

def test_user_create(client:TestClient, db:Session):
    data = utils.create_random_user_dict()

    response= client.post(f"/api/v1/user", json=data)
    
    assert response.status_code == 201
    content = response.json()
    assert "id" in content

    for key in data.keys():
        assert content[key] == data[key]


def test_user_read(client:TestClient, db:Session):
    user_dict = utils.create_random_user_dict()
    data = utils.create_user(db, user_dict)

    response= client.get(f"/api/v1/user/{data['id']}")
    content = response.json()
    assert response.status_code == 200
    
    for key in data.keys():
        assert content[key] == data[key]

def test_users_food_logs(client:TestClient, db:Session):
    user_dict = utils.create_random_user_dict()
    user = utils.create_user(db, user_dict)

    food = utils.create_random_food(db)
    serving = utils.create_random_serving_size(food['id'], db)
    date = utils.random_date()

    log = utils.create_food_log(user['id'], food['id'], serving['id'], date, db)


    response= client.get(f"/api/v1/user/{user['id']}")
    assert response.status_code == 200

    content = response.json()
    for key in user.keys():
        assert content[key] == user[key]


    for key in log.keys():
        assert content['log'][-1][key] == log[key]

    assert content['log'][-1]['food'] == food
    assert content['log'][-1]['serving_size'] == serving