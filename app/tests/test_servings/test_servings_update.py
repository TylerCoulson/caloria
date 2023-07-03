async def test_update_serving_size_success(client, update_serving):
    # Test case 1: Successful update
    response = await client.put(f"/api/v1/food/{update_serving['food_id']}/serving/{update_serving['id']}", json=update_serving)
    assert response.status_code == 200
    assert response.json() == update_serving

async def test_update_serving_size_invalid_id(client, update_serving):
    # Test case 2: Invalid serving ID
    response = await client.put("/api/v1/food/1/serving/9999", json=update_serving)
    assert response.status_code == 404
    assert response.json() == {"detail": "Serving size not found"}

async def test_update_serving_size_invalid_data(client):
    # Test case 3: Invalid serving size data
    response = await client.put("/api/v1/food/1/serving/1", json={"serving_size_in": {"invalid_key": 10}})
    assert response.status_code == 422
    assert "detail" in response.json() 