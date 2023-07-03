async def test_update_food_valid_data(client, update_food):
    # Test case: Updating food with valid data
    response = await client.put("/api/v1/food/1", json=update_food)
    assert response.status_code == 200
    assert response.json() == update_food

async def test_update_food_invalid_food_id(client, update_food):
    # Test case: Updating food with invalid food_id
    response = await client.put("/api/v1/food/asdf", json=update_food)
    assert response.status_code == 422
    assert "detail" in response.json()

async def test_update_food_missing_data(client):
    # Test case: Updating food with missing data
    response = await client.put("/api/v1/food/2", json={})
    assert response.status_code == 422
    assert "detail" in response.json()

async def test_update_food_nonexistent_food_id(client, update_food):
    # Test case: Updating food with non-existent food_id
    response = await client.put("/api/v1/food/9999", json=update_food)
    assert response.status_code == 404
    assert "detail" in response.json()
