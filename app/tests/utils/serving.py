import pytest
from app import models, schemas, crud

@pytest.fixture()
async def create_serving() -> models.ServingSize:
    serving = {
        "id": 1001,
        "food_id": 1,
        "description": 'nisi volutpat',
        "calories": 6121,
        "fats": 302,
        "carbs": 750,
        "protein": 372,
        "food": {"id": 1, "category_id": 2, "type": 'posuere', "subtype": 'viverra dapibus', "user_id": 1001}
    } 
    return serving

@pytest.fixture()
async def get_serving() -> models.ServingSize:
    serving = {"id": 13, "food_id": 13, "description": 'lacus', "calories": 186, "fats": 369, "carbs": 764, "protein": 994}
    food = {"id": 13, "category_id": 6, "type": 'fermentum justo nec', "subtype": None, "user_id": 1001}
    return {**serving, 'food':food}

@pytest.fixture()
async def get_multiple_serving() -> models.ServingSize:
    serving = {'food_id': 1, 'description': 'nisi volutpat', 'calories': 6121, 'fats': 302, 'carbs': 750, 'protein': 372, 'id': 1}
    return {"servings":[serving]}

@pytest.fixture()
async def update_serving() -> models.ServingSize:
    serving = {"id": 1, "food_id": 17, "description": 'amet', "calories": 9602, "fats": 332, "carbs": 571, "protein": 856}
    food = {"id": 17, "category_id": 3, "type": 'nec sem', "subtype": 'magna', "user_id": 1001}
    return {**serving, 'food':food}

@pytest.fixture()
async def delete_serving() -> models.ServingSize:
    serving = {"id": 1, "category_id": 2, "type": 'odio porttitor', "subtype": 'nec'}
    return serving