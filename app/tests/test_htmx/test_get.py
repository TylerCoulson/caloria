import pytest
from sqlalchemy.orm import Session
from fastapi.testclient import TestClient
from app.tests.test_htmx.htmx_utils import methods, weight_params

@pytest.mark.parametrize(
        "url",
        methods['GET']
)
async def test_gets(client:TestClient, url):
    params = {"food_category": 1, "search_word":"test", "food_id":1, "log_id":1, **weight_params, "email":"test123@test.com","password":"1231412321", "password_confirm":"1231412321"}
    response = await client.get(url, params=params)

    assert response.status_code == 200
    assert response.headers["content-type"] == "text/html; charset=utf-8"