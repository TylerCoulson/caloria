from sqlalchemy.orm import Session
from fastapi.testclient import TestClient
from fastapi.encoders import jsonable_encoder
from app.crud import crud
from app import models
from app import schemas
from datetime import date

from . import utils

def test_recipe_create(client:TestClient, db:Session):
    food_1 = utils.create_random_food(db)
    food_2 = utils.create_random_food(db)

    data = {
        "finished_food": food_1['id'],
        "ingredient": food_2['id']
    }
    
    response= client.post("/recipe", json=data)

    assert response.status_code == 201
    content = response.json()
    

    assert "ingredients" in content

    assert content['ingredients'][0]["id"] == data['ingredient']
