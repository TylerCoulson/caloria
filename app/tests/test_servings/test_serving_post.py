async def test_post_serving_size_success(client, create_serving):
    # Test case: Successful creation of serving size
    response = await client.post(f"/api/v1/food/{create_serving['food_id']}/serving", json=create_serving)
    assert response.status_code == 201
    
    assert response.json() == create_serving

async def test_post_serving_size_missing_fields(client, create_serving):
    # Test case: Missing required fields
    serving_size_data = {"name": "Small"}
    response = await client.post(f"/api/v1/food/{create_serving['food_id']}/serving", json=serving_size_data)
    assert response.status_code == 422

async def test_post_serving_size_invalid_food_id(client, create_serving):
    # Test case: Invalid food_id
    response = await client.post("/api/v1/food/invalid_food_id/serving/", json=create_serving)
    assert response.status_code == 307