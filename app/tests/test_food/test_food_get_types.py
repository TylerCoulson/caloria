async def test_get_food_types(client):
    response = await client.get("/api/v1/food/types")
    assert response.status_code == 200
    assert len(response.json()) == 25

async def test_get_food_subtypes(client, get_food):
    response = await client.get(f"/api/v1/food/{get_food['type']}/subtypes")
    assert response.status_code == 200
    assert isinstance(response.json(), list) 