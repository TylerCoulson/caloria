import pytest
from sqlalchemy.orm import Session
from fastapi.testclient import TestClient
from app.tests.test_htmx.htmx_utils import methods

@pytest.mark.parametrize(
        "url",
        methods['PUT']
)
async def test_put(client:TestClient, db:Session, url):
    data = {
        # profile
        "id":2, "start_date": '2023-12-06', "start_weight": 321.4, "goal_weight": 151.0, "sex": 'Female', "birthdate": '1992-12-05', "height": 70, "lbs_per_week": 1.0, "activity_level": 1.2, "user_id": 2,
        # food_log
        "id":100, "date":'2023-04-27', "food_id":123, "serving_size_id":123, "serving_amount":4.0, "profile_id":1,
        # food
        "id":1, "category_id":2, "type":"this one", "subtype":"that one", "user_id":1001,
        # serving
        "id":1, "calories":100, "carbs":300, "fats":200, "protein": 400, "description":"Tspadlknf"
    }
    response = await client.put(url, json=data)

    assert response.status_code == 200
    assert response.headers["content-type"] == "text/html; charset=utf-8"