async def test_post_food_success(client, create_food):
    # Test case: Successful creation of food
    response = await client.post("/api/v1/food", json=create_food)
    assert response.status_code == 201
    assert response.json() == create_food

async def test_post_food_missing_data(client):
    # Test case: Missing food data
    response = await client.post("/api/v1/food", json={})
    assert response.status_code == 422
    assert "detail" in response.json()
