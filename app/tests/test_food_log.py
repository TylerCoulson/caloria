from sqlalchemy.orm import Session
from fastapi.testclient import TestClient
from fastapi.encoders import jsonable_encoder
from app.crud import crud
from app import models
from app import schemas
from datetime import date
from . import utils

def test_food_log_create(client:TestClient, db:Session):
    user_dict = utils.create_random_user_dict()
    user = utils.create_user(db, user_dict)
    
    food = utils.create_random_food(db)
    servings = utils.create_random_serving_size(food['id'], db)


    data = {
        "date": date(2023,1,23).isoformat(), 
        "food_id": food['id'],
        "serving_size_id": servings['id'],
        "serving_amount": 1,
        "user_id": user['id']
    }

    response= client.post(f"/api/v1/food_log", json=data)
    assert response.status_code == 201
    content = response.json()
    assert "id" in content
    assert "food" in content
    assert "serving_size" in content
    for key in data.keys():
        assert content[key] == data[key]

def test_food_log_read_id(client:TestClient, db:Session):
    user_dict = utils.create_random_user_dict()
    user = utils.create_user(db, user_dict)
    food = utils.create_random_food(db)
    servings = utils.create_random_serving_size(food['id'], db)

    data = {
        "date": date(2023,1,23).isoformat(), 
        "food_id": food['id'],
        "serving_size_id": servings['id'],
        "serving_amount": 1,
        "user_id": user['id']
    }


    input_data = schemas.FoodLogCreate(**data)
    output_data = crud.create(obj_in=input_data, db=db, model=models.Food_Log)


    response= client.get(f"/api/v1/food_log/{output_data.id}")

    assert response.status_code == 200
    content = response.json()
    for key in data.keys():
        assert content[key] == data[key]
    
    assert content["food"] == food
    assert content["serving_size"] == servings
    assert content["user"] == user

def test_food_log_read_day(client:TestClient, db:Session):
    user_dict = utils.create_random_user_dict()
    user = utils.create_user(db, user_dict)
    food = utils.create_random_food(db)
    servings = utils.create_random_serving_size(food['id'], db)

    data = {
        "date": date(2023,1,23).isoformat(), 
        "food_id": food['id'],
        "serving_size_id": servings['id'],
        "serving_amount": 1,
        "user_id": user['id']
    }

    full_output_date = []
    to_delete = []
    for i in range(2):

        input_data = schemas.FoodLogCreate(**data)
    
        output_data = crud.create(obj_in=input_data, db=db, model=models.Food_Log)

        to_delete.append(output_data)
        full_output_date.append(jsonable_encoder(output_data))

    response= client.get(f"/api/v1/food_log/{user['id']}/date/{data['date']}")

    assert response.status_code == 200
    
    full_output_date[-1]["food"] = food
    full_output_date[-1]["serving_size"] = servings
    
    content = response.json()

    assert content['user'] == user
    assert content['log'][-1] == full_output_date[-1]
    
    # deletes created entries so test can be rerun without deleting database
    for i in to_delete:
        crud.delete(_id = i.id, db=db, db_obj=i)