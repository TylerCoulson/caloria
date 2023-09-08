import pytest
from app import models, schemas, crud

@pytest.fixture()
async def create_food() -> models.Food:
    food = {"id": 1001, "category_id": 2, "type": 'odio porttitor', "subtype": 'nec', 'category': {'description': 'Fast Food', 'id': 2}}
    return food

@pytest.fixture()
async def get_food() -> models.Food:
    food = {"id": 1, "category_id": 2, "type": 'posuere', "subtype": 'viverra dapibus', 'category': {'description': 'Fast Food', 'id': 2}}
    return food

@pytest.fixture()
async def update_food() -> models.Food:
    food = {"id": 1, "category_id": 2, "type": 'odio porttitor', "subtype": 'nec', 'category': {'description': 'Fast Food', 'id': 2}}
    return food

@pytest.fixture()
async def delete_food() -> models.Food:
    food = {"id": 1, "category_id": 2, "type": 'odio porttitor', "subtype": 'nec'}
    return food