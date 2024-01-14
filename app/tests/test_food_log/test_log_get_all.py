async def test_get_all_logs_default(client):
    response = await client.get("/api/v1/food_log")
    assert response.status_code == 200
    assert len(response.json()) == 25

async def test_get_all_logs_custom(client):
    response = await client.get("/api/v1/food_log?n=10&page=2")
    assert response.status_code == 200
    assert len(response.json()) == 10

async def test_get_all_logs_invalid_n(client):
    # invalid options default to the first page 
    response = await client.get("/api/v1/food_log?n=-5")
    assert response.status_code == 200
    assert len(response.json()) == 25

async def test_get_all_logs_invalid_page(client):
    # invalid options default to the first page 
    response = await client.get("/api/v1/food_log?page=-34")
    assert response.status_code == 200
    assert len(response.json()) == 25