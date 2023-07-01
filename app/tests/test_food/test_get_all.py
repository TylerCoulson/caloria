

async def test_get_all_foods_default(client):
    response = await client.get("/api/v1/food/all")
    assert response.status_code == 200
    assert len(response.json()) == 25

async def test_get_all_foods_custom(client):
    response = await client.get("/api/v1/food/all?n=10&page=2")
    assert response.status_code == 200
    assert len(response.json()) == 10


async def test_get_all_foods_invalid_n(client):
    # invalid options default to the first page 
    response = await client.get("/api/v1/food/all?n=-5")
    assert response.status_code == 200
    assert len(response.json()) == 25

async def test_get_all_foods_invalid_page(client):
    # invalid options default to the first page 
    response = await client.get("/api/v1/food/all?page=-34")
    assert response.status_code == 200
    assert len(response.json()) == 25