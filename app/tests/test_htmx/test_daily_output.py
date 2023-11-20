import datetime
from sqlalchemy.orm import Session
from fastapi.testclient import TestClient

async def test_create_daily(client:TestClient, db:Session):
    # Test case 1: Test with current date
    response = await client.get("/daily/create/" + str(datetime.date.today()))
    assert response.status_code == 200
    assert response.headers["content-type"] == "text/html; charset=utf-8"

async def test_create_specific_date(client:TestClient, db:Session):
    # Test case 2: Test with a specific date
    response = await client.get("/daily/create/2022-01-01")
    assert response.status_code == 200
    assert response.headers["content-type"] == "text/html; charset=utf-8"

async def test_with_an_invalid_date_format(client:TestClient, db:Session):
    # Test case 3: Test with an invalid date format
    response = await client.get("/daily/create/01-01-2022")
    assert response.status_code == 422