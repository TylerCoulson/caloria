from sqlalchemy.orm import Session
from fastapi.testclient import TestClient
from fastapi.encoders import jsonable_encoder
from app.crud import crud
from app import models
from app import schemas
from datetime import date

def test_food_create(client:TestClient, db:Session):
    data = {
        "brand": "generic",
        "name": "test123"
    }

    response= client.post(f"/api/v1/food", json=data)

    assert response.status_code == 201
    content = response.json()
    assert "id" in content

    for key in data.keys():
        assert content[key] == data[key]

def test_food_read(client:TestClient, db:Session, food:schemas.Food):
    # data = {
    #     "brand": "read_test",
    #     "name": "test123"
    # }

    # input_data = schemas.FoodCreate(**data)
    
    # output_data = crud.create(obj_in=input_data, db=db, model=models.Food)

    response= client.get(f"/api/v1/food/{food.id}")
    assert response.status_code == 200
    assert response.json() == {
        "id": food.id,
        "brand": food.brand,
        "name": food.name,
        "ingredients": []
    }
