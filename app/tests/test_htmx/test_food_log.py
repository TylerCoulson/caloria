import datetime
from sqlalchemy.orm import Session
from fastapi.testclient import TestClient
import pytest

update_data = {"id":100, "date":'2023-04-27', "food_id":123, "serving_size_id":123, "serving_amount":4.0, "profile_id":1}
create_data = {"id":1001, "date":'2022-12-09', "food_id":123, "serving_size_id":123, "serving_amount":3, "profile_id":1}

async def test_get_log(client:TestClient, db:Session):
    response = await client.get(f"/food_log")
    assert response.status_code == 200
    assert response.headers["content-type"] == "text/html; charset=utf-8"

async def test_get_log_create(client:TestClient, db:Session):
    response = await client.get(f"/food_log/create", params={"food_id":1})
    assert response.status_code == 200
    assert response.headers["content-type"] == "text/html; charset=utf-8"

@pytest.mark.parametrize(
    "log_id, copy, status_code",
    [
        (1, False, 200),
        (1, True, 200),
    ]
)
async def test_get_log_edit(client:TestClient, db:Session, log_id, copy, status_code):
    response = await client.get(f"/food_log/edit", params={"log_id":log_id, "copy":copy})
    assert response.status_code == status_code
    assert response.headers["content-type"] == "text/html; charset=utf-8"

async def test_get_log_id(client:TestClient, db:Session):
    response = await client.get(f"/food_log/1")
    assert response.status_code == 200
    assert response.headers["content-type"] == "text/html; charset=utf-8"

async def test_get_log_date(client:TestClient, db:Session):
    response = await client.get(f"/food_log/2022-10-09")
    assert response.status_code == 200
    assert response.headers["content-type"] == "text/html; charset=utf-8"

async def test_update_log(client:TestClient, db:Session):
    response = await client.put(f"/food_log/1", json=update_data)
    assert response.status_code == 200
    assert response.headers["content-type"] == "text/html; charset=utf-8"

async def test_create_log(client:TestClient, db:Session):
    response = await client.post(f"/food_log", json=create_data)
    assert response.status_code == 200
    assert response.headers["content-type"] == "text/html; charset=utf-8"

async def test_delete_log(client:TestClient, db:Session):
    response = await client.delete(f"/food_log/1")
    assert response.status_code == 200
    assert response.text == "null"