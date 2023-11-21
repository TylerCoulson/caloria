import pytest
from sqlalchemy.orm import Session
from fastapi.testclient import TestClient
from app.tests.test_htmx.htmx_utils import methods

@pytest.mark.parametrize(
        "url",
        methods['POST']
)
async def test_post(client:TestClient, db:Session, url):
    data = {
        # food
        "id": 1001, "category_id": 2, "type": 'odio porttitor', "subtype": 'nec', 'category': {'description': 'Fast Food', 'id': 2}, "user_id": 1001,
        # servings
        "id": 1001, "food_id": 1, "description": 'nisi volutpat', "calories": 6121, "fats": 302, "carbs": 750, "protein": 372, "food": {"id": 1, "category_id": 2, "type": 'posuere', "subtype": 'viverra dapibus', "user_id": 1001},
        # food log
        "id":1001, "date":'2022-12-09', "food_id":123, "serving_size_id":123, "serving_amount":3, "profile_id":1
    }

    response = await client.post(url, json=data)

    assert response.status_code == 200
    assert response.headers["content-type"] == "text/html; charset=utf-8"