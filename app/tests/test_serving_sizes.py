from sqlalchemy.orm import Session
from fastapi.testclient import TestClient
from fastapi.encoders import jsonable_encoder
from app.crud import crud
from app import models
from app import schemas


def test_serving_size_create(client:TestClient, db:Session):
    data = {
        "food_id": 1,
        "description": "100g",
        "calories": 321,
        "fats": 11,
        "carbs": 41,
        "protein": 13,
    }

    response= client.post(f"/api/v1/serving_size", json=data)
    
    assert response.status_code == 201
    content = response.json()
    assert "id" in content

    for key in data.keys():
        assert content[key] == data[key]

def test_serving_size_read_id(client:TestClient, db:Session, serving: models.ServingSize):
    # data = {
    #     "food_id": 1,
    #     "description": "100g",
    #     "calories": 321,
    #     "fats": 11,
    #     "carbs": 41,
    #     "protein": 13,
    # }

    # input_data = schemas.ServingSizeCreate(**data)
    
    # output_data = crud.create(obj_in=input_data, db=db, model=models.ServingSize)

    response= client.get(f"/api/v1/serving_size/{serving.id}")
    assert response.status_code == 200
    
    content = response.json() 
    assert content == jsonable_encoder(serving) 

def test_serving_size_read_by_food(client:TestClient, db:Session):
    data = {
        "food_id": 37,
        "description": "100g",
        "calories": 321,
        "fats": 11,
        "carbs": 41,
        "protein": 13,
    }
    
    full_output_date = []
    to_delete = []
    for i in range(10):

        input_data = schemas.ServingSizeCreate(**data)
        
        output_data = crud.create(obj_in=input_data, db=db, model=models.ServingSize)
        to_delete.append(output_data)
        full_output_date.append(jsonable_encoder(output_data))
        

    response= client.get(f"/api/v1/serving_size/food_id/{output_data.food_id}")
    assert response.status_code == 200
    assert response.json() == {"servings":full_output_date}

