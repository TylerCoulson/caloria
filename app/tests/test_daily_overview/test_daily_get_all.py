from fastapi.testclient import TestClient
from datetime import timedelta, datetime


async def test_daily_overview_get_all_default(client:TestClient, module_profile):    

    response= await client.get(f"/api/v1/daily")

    assert response.status_code == 200
    content = response.json()
    assert len(content) == 25

async def test_daily_overview_get_all_custom(client):
    response = await client.get("/api/v1/daily?n=10&page=2")
    assert response.status_code == 200
    assert len(response.json()) == 10


async def test_get_all_foods_invalid_n(client):
    # invalid options default to the first page 
    response = await client.get("/api/v1/daily?n=-5")
    assert response.status_code == 200
    assert len(response.json()) == 25

async def test_get_all_foods_invalid_page(client):
    # invalid options default to the first page 
    response = await client.get("/api/v1/daily?page=-34")
    assert response.status_code == 200
    assert len(response.json()) == 25