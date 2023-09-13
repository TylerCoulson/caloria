async def test_get_serving_size_by_food_exists(client, get_multiple_serving):
    # Test when food_id exists in the database
    response = await client.get("/api/v1/food/1/servings")
    assert response.status_code == 200
    assert response.json() == get_multiple_serving


async def test_get_serving_size_by_food_not_exists(client):
    # Test when food_id does not exist in the database
    response = await client.get("/api/v1/food/9999/servings")
    assert response.status_code == 404
    assert response.json()["detail"] == "Food not found"


async def test_get_serving_size_by_food_negative(client):
    # Test when food_id is a negative value
    response = await client.get("/api/v1/food/-1/servings")
    assert response.status_code == 404
    assert response.json()["detail"] == "Food not found"


async def test_get_serving_size_by_food_zero(client):
    # Test when food_id is zero
    response = await client.get("/api/v1/food/0/servings")
    assert response.status_code == 404
    assert response.json()["detail"] == "Food not found"


async def test_get_serving_size_by_food_string(client):
    # Test when food_id is a string
    response = await client.get("/api/v1/food/abc/servings")
    assert response.status_code == 422