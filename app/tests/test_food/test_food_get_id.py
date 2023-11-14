async def test_get_food_by_id_returns_food_when_found(client, get_food):

    response = await client.get(f"/api/v1/food/{get_food['id']}")
    assert response.status_code == 200
    assert response.json() == get_food

async def test_get_food_by_id_raises_404_when_food_not_found(client):
    response = await client.get(f"/api/v1/food/10000")
    assert response.status_code == 404
    assert response.json()["detail"] == "Food not found"