import datetime
from sqlalchemy.orm import Session
from fastapi.testclient import TestClient
import pytest

async def test_create_daily(client:TestClient, db:Session):
    response = await client.get(f"/daily/create/{datetime.date.today()}")
    assert response.status_code == 200
    assert response.headers["content-type"] == "text/html; charset=utf-8"

async def test_create_specific_date(client:TestClient, db:Session):
    response = await client.get("/daily/create/2022-01-01")
    assert response.status_code == 200
    assert response.headers["content-type"] == "text/html; charset=utf-8"

async def test_with_an_invalid_date_format(client:TestClient, db:Session):
    response = await client.get("/daily/create/01-01-2022")
    assert response.status_code == 422

async def test_create_daily_activity_level(client:TestClient, db:Session):
    response = await client.get(f"/daily/create/{datetime.date.today()}/activity_level")
    assert response.status_code == 200
    assert response.headers["content-type"] == "text/html; charset=utf-8"


async def test_get_daily(client:TestClient, db:Session):
    response = await client.get(f"/daily")
    assert response.status_code == 200
    assert response.headers["content-type"] == "text/html; charset=utf-8"

async def test_get_daily_date(client:TestClient, db:Session):
    response = await client.get(f"/daily/{datetime.date.today()}")
    assert response.status_code == 200
    assert response.headers["content-type"] == "text/html; charset=utf-8"

@pytest.mark.parametrize(
    "actual_weight, activity_level, status_code",
    [
        (True, False, 200),
        (False, True, 200),
    ]
)
async def test_update_actual_weight(client:TestClient, db:Session, actual_weight, activity_level, status_code):
    response = await client.put(
        f"/daily/{datetime.date.today()}",
        params={
            "actual_weight": actual_weight,
            "activity_level": activity_level
        },
        json={
            "actual_weight": 70,
            "activity_level": 1.4
        }
    )
    assert response.status_code == status_code
    assert response.headers["content-type"] == "text/html; charset=utf-8"